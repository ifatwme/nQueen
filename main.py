import pygame
from PIL import Image
import random
import sys
import argparse
import time


class Queen():
    def __init__(self, id, position:tuple, square_size):
        self.id = id
        self.position = position
        self.x = self.position[0] * square_size
        self.y = self.position[1] * square_size


class QueenProblem():
    # x, y = 0, 0 # col:(right+, left-), row:(up-, down+)
    def __init__(self, n, seed, square_size, speed, image_path):
        self.queen_positions = []
        self.n = n
        self.square_size = square_size
        self.speed = speed
        # Initialize positions
        self.positions = [(col, row) for col in range(self.n) for row in range(self.n)]
        self.queen_positions = [(col, 0) for col in range(self.n)]
        if seed:
            random.seed(seed)
            rows = random.sample(range(self.n), self.n)
            self.queen_positions = [(col, rows[col]) for col in range(self.n)]
        # Ready the screen for game to play
        self.screen = pygame.display.set_mode(size=((self.square_size * self.n) + 50, (self.square_size * self.n) + 50))
        pygame.init()
        pygame.display.set_caption("N-Queens Problem")
        self.preprocess_image(image_path)
        self.queen_image = pygame.image.load("queen.png")
        self.conflict = 0
        self.draw_board()
        self.queens = self.initial_queens()
        for queen in self.queens:
            self.screen.blit(self.queen_image, (queen.x, queen.y))
            pygame.display.flip()
        pygame.display.update()
    

    def preprocess_image(self, image_path):
        queen_image = Image.open(image_path)
        queen_image = queen_image.convert("RGBA")
        # Get the alpha channel (transparency) of the image
        alpha = queen_image.split()[3]
        # Make a copy of the alpha channel with a threshold to remove the white background
        threshold = 200
        alpha = alpha.point(lambda p: p > threshold and 255)
        # Paste the alpha channel back into the image
        queen_image.putalpha(alpha)
        queen_image = queen_image.resize((self.square_size, self.square_size), Image.LANCZOS)
        # Paste the queen image onto the square
        queen_image.paste(queen_image, (0, 0))
        queen_image.save("queen.png")
    
    
    def start(self):
        start_time = time.time()
        while (time.time() - start_time) < 10:
            user_input = input("Starting the game within 10 seconds: ")
            if user_input == '':
                break
        print("Game is starting now!")

        running = True
        calculating = True
        flaga = 1

        while running:
            pygame.time.delay(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if not calculating:
                self.draw_board()
                for i in range(self.n):
                    self.screen.blit(self.queen_image, (self.queen_positions[i][0]*self.square_size, self.queen_positions[i][1]*self.square_size))
                pygame.display.flip()
                start_time = time.time()
                while (time.time() - start_time) < 10:
                    user_input = input("Finished closing the game within 10 seconds: ")
                    if user_input == '':
                        return

            else:
                calculating, flaga = self.find_solution(calculating, flaga)
                for i in range(self.n):
                    self.move(self.queens[i], self.queen_positions[i])
                    pygame.display.flip()

            pygame.display.update()
        pygame.quit()
        sys.exit()


    def draw_board(self):
        self.screen.fill((200, 200, 200))
        self.conflict = self.count_conflicts(self.queen_positions)
        self.screen.blit(pygame.font.Font(None, 30).render('Conflicts= {}'.format(str(self.conflict)), True, (200, 0, 0)), (0, (self.square_size * self.n) + 20))
        for position in self.positions:
            color = (255, 255, 255) if (position[1] + position[0]) % 2 == 0 else (64, 64, 64)
            pygame.draw.rect(
                self.screen,
                color,
                (
                    position[0] * self.square_size,
                    position[1] * self.square_size,
                    self.square_size,
                    self.square_size,
                ),
            )
            if position not in self.queen_positions:
                self.screen.blit(pygame.font.Font(None, 25).render(str(self.count_conflicts_square(position)[0]), True, (200, 0, 0)), (position[0] * self.square_size, position[1] * self.square_size))


    def initial_queens(self):
        return [Queen(position[0], position, self.square_size) for position in self.queen_positions]


    def count_conflicts(self, queen_positions):
        counts = 0
        for col1 in range(self.n):
            for col2 in range(col1, self.n):
                if self.attackDiagonal(queen_positions[col1], queen_positions[col2]):
                    counts += 1
                if self.attackRow(queen_positions[col1], queen_positions[col2]):
                    counts += 1
                if self.attackCol(queen_positions[col1], queen_positions[col2]):
                    counts += 1
        return counts
    

    def count_conflicts_square(self, position):
        qps = self.queen_positions.copy()
        for queen_position in qps:
            if position[0] == queen_position[0]:
                qps[position[0]] = position
                break
        return self.count_conflicts(qps), qps
    

    def attackDiagonal(self, position, queen_position):
        if (queen_position != position) and abs(queen_position[0]-position[0]) == abs(queen_position[1]-position[1]):
            return True


    def attackRow(self, position, queen_position):
        if (queen_position != position) and position[1] == queen_position[1]:
            return True


    def attackCol(self, position, queen_position):
        if (queen_position != position) and position[0] == queen_position[0]:
            return True
    

    def find_solution(self, calculating, flaga):
        if self.conflict == 0:
            calculating = False
            return calculating, flaga
        min_conflict = (self.n * (self.n-1)) / 2
        min_queen_positions = self.queen_positions
        temp = self.positions[(flaga-1)*self.n:flaga*self.n]
        for position in temp:
            if position not in self.queen_positions:
                cft, qps = self.count_conflicts_square(position)
                if min_conflict > cft:
                    min_conflict = cft
                    min_queen_positions = qps
        self.queen_positions = min_queen_positions
        flaga += 1
        if flaga == self.n+1:
            flaga = 1
        return calculating, flaga


    def move(self, queen, position:tuple):
        dx, dy = queen.position[0] - position[0], queen.position[1] - position[1]
        if dx != 0: # up, down
            for _ in range(abs(dx)):
                for _ in range(self.speed):
                    self.draw_board()
                    for i in range(self.n):
                        if i == queen.id:
                            continue
                        self.screen.blit(self.queen_image, (self.queen_positions[i][0]*self.square_size, self.queen_positions[i][1]*self.square_size))
                    self.screen.blit(self.queen_image, (queen.x, queen.y))
                    if dx < 0:
                        queen.x += self.square_size / (self.speed)
                    elif dx > 0:
                        queen.x -= self.square_size / (self.speed)
                    pygame.display.flip()
                    pygame.display.update()
        elif dx == 0:
            self.screen.blit(self.queen_image, (queen.x, queen.y))
            pygame.display.flip()
            pygame.display.update()
        queen.position = (position[0], queen.position[1])

        if dy != 0: # up, down
            for _ in range(abs(dy)):
                for _ in range(self.speed):
                    self.draw_board()
                    for i in range(self.n):
                        if i == queen.id:
                            continue
                        self.screen.blit(self.queen_image, (self.queen_positions[i][0]*self.square_size, self.queen_positions[i][1]*self.square_size))
                    self.screen.blit(self.queen_image, (queen.x, queen.y))
                    if dy < 0:
                        queen.y += self.square_size / (self.speed)
                    elif dy > 0:
                        queen.y -= self.square_size / (self.speed)
                    pygame.display.flip()
                    pygame.display.update()
        elif dy == 0:
            self.screen.blit(self.queen_image, (queen.x, queen.y))
            pygame.display.flip()
            pygame.display.update()
        queen.position = (queen.position[0], position[1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Give the nQueen some parameter, you can keep it as default too!')
    parser.add_argument('-n', '--nqueen', type=int, default=8, help='Number of queens.')
    parser.add_argument('-r', '--seed', type=int, default=0, help='Start from zero, otherwise initialize randomly with seed.')
    parser.add_argument('-s', '--screen', type=int, default=100, help='Size of screen.')
    parser.add_argument('-p', '--speed', type=int, default=30, help='Speed of moving the queens.')

    args = parser.parse_args()

    problem = QueenProblem(args.nqueen, args.seed, args.screen, args.speed, image_path='queen_h.png')
    problem.start()