# Graphical Implementation of N-Queen with Pygame
## Introduction
Under the guidance of Professor **Farsad Boroujeni Zamani**,
I have implemented nQueen problem with a nice user interface and a default algrithm which is,

algorithm: each queen moves only up and down in its column and in each iteration queens move toward the least conflict when is's their turn.

Different algorithms can be added like: Backtracking(csp), genetic algorithm, simulated annealing and more. For this you can add your desired `find_solution()` method to the code.

## Requirements
The rqueirements for this project can be found in the **rquirements.txt**, which can be installed in two ways:
### Conda
```
$ conda activate your_environment_name
$ conda install --file requirements.txt
```
### venv
```
$ python3 -m venv your_virtual_env
$ pip install -r requirements.txt
```

## Commands
You may start the game with the following command in a terminal:


This command will runs with the defaults:
+ n: **8**
+ seed: **0** (no seed)
+ screen: **100**
+ speed: **30**
```
$ python main.py
```
**NOTICE**: when you start the project with the above command at the end and the start of the project will ask you to **press the Enter** in order to start the game or close the game, otherwise it will start or close itself within **10 seconds**!

The game can also be paramterized like this command:
```
$ python main.py -n 5 -r 42 -s 80 -p 30
```
