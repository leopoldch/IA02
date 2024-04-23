""" IA02 TP4 - TicTacToe"""

from typing import Callable
import os
import math
import time
import random

def clear():
    """clear console"""
    os.system("clear")

# Defined types
Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[Grid, Player], Action]


def grid_tuple_to_grid_list(grid: Grid) -> list[list[int]]:
    """Converting tuple to grid"""
    main_grid: list[list[int]] = []
    for element in grid:
        semi_tab: list[int] = []
        for item in element:
            semi_tab.append(item)
        main_grid.append(semi_tab)
    return main_grid


def grid_list_to_grid_tuple(grid: list[list[int]]) -> Grid:
    """Converting grid to tuple"""
    main_grid = grid
    for i, item in enumerate(main_grid):
        main_grid[i] = tuple(item)
    return tuple(main_grid)


def check_line(grid: State, player: Player) -> bool:
    """check line by line if a player has won"""
    for item in grid:
        if item[0] == item[1] == item[2] == player:
            return True
    return False


def check_col(grid: State, player: Player) -> bool:
    """check column by column if a player has won"""
    for i in range(3):
        if grid[0][i] == grid[1][i] == grid[2][i] == player:
            return True
    return False


def check_diag(grid: State, player: Player) -> bool:
    """check diagonals if a player has won"""
    return (grid[0][0] == grid[1][1] == grid[2][2] == player) or (
        grid[0][2] == grid[1][1] == grid[2][0] == player
    )


def line(grid: State, player: Player) -> bool:
    """verify if player has 3 items aligned"""
    return (
        check_line(grid, player) or check_col(grid, player) or check_diag(grid, player)
    )


def final(grid: State) -> bool:
    """verify if a player has won"""
    # players can be 1 or 2
    verif: bool = not legals(grid)
    return line(grid, 1) or line(grid, 2) or verif


def score(grid: State) -> float:
    """returns"""
    if line(grid, 1) or line(grid, 2):
        return 1
    return 0


def pprint(grid: State):
    """prints grid"""
    for line_value in grid:
        for item in line_value:
            if item == 0:
                print(" *", end=" ")
            elif item == 1:
                print(" X", end=" ")
            elif item == 2:
                print(" O", end=" ")
            else:
                raise ValueError("Erreur de données dans la grille")
        print()


def legals(grid: State) -> list[Action]:
    """returns available actions"""
    actions: list[Action] = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                actions.append([i, j])
    return actions


def play(grid: State, player: Player, action: Action) -> State:
    """effectuer une action si elle est possible"""
    my_grid = grid_tuple_to_grid_list(grid)
    if list(action) in legals(grid):
        my_grid[action[0]][action[1]] = player
        return grid_list_to_grid_tuple(my_grid)

    raise ValueError("action impossible")


def input_to_action(my_input: int) -> Action:
    """convert input to action"""
    col = my_input % 3
    l = math.floor(my_input / 3)
    action: Action = [l, col]
    return action


def strategy_brain(grid: Grid, player: Player) -> Action:
    """Startegy real player"""
    clear()
    print("Grid State : \n")
    pprint(grid)
    print("\n")
    print(f"Joueur {player} à vous de jouer: ", end="\n")
    print("Chaque case est représentée par un chiffre")
    s = int(input("Veuillez rentrer un chiffre entre 0 et 8 : "))
    while s > 8 or s < 0:
        clear()
        print("Grid State : \n")
        pprint(grid)
        print("\n")
        print(f"Joueur {player} à vous de jouer: ", end="\n")
        print("VEUILLEZ RENSEIGNER UNE CASE VALIDE")
        print("Chaque case est représentée par un chiffre")
        s = int(input("Veuillez rentrer un chiffre entre 0 et 8 : "))
    return input_to_action(s)


def strategy_first_legal(grid: State, player: Player) -> Action:
    """strategy first legal choice"""
    legals_choices: list[Action] = legals(grid)
    choice : Action = legals_choices[0]
    print(f"\nChoix du joueur {player} : {choice}")
    time.sleep(1.5)
    return choice


def strategy_random(grid: State, player: Player) -> Action:
    """strategy random choice"""
    legals_choices: list[Action] = legals(grid)
    nb: int = random.randint(0, len(legals_choices) - 1)
    choice : Action = legals_choices[nb]
    print(f"\nChoix du joueur {player} : {choice}")
    time.sleep(1.5)
    return choice


def tictactoe(strategy_x: Strategy, strategy_o: Strategy, debug: bool = False) -> Score:
    """main game function"""
    grid: State = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    player1: Player = 1
    player2: Player = 2
    current: Player = 1
    while final(grid) == debug:
        if current == player1:
            action: Action = strategy_x(grid, player1)
            try:
                grid = play(grid, player1, action)
            except ValueError:
                clear()
                print(
                    "\n\nAction impossible, la case est déjà prise, retentez votre coup"
                )
                time.sleep(1.5)
                current: Player = 2  # permet de ne pas changer de joueur à l'exception
        else:
            action: Action = strategy_o(grid, player2)
            try:
                grid = play(grid, player2, action)
            except ValueError:
                clear()
                print(
                    "\n\nAction impossible, la case est déjà prise, retentez votre coup"
                )
                time.sleep(1.5)
                current: Player = 1  # permet de ne pas changer de joueur à l'exception
        if current == player1:
            current = player2
        else:
            current = player1
    clear()
    print("Grid State : \n")
    pprint(grid)
    if line(grid, player1):
        print("\nLe joueur1 gagne !")
    elif line(grid, player2):
        print("\nLe joueur2 gagne !")
    else:
        print("\n=============== MATCH NUL ===============")


tictactoe(strategy_brain, strategy_random)
