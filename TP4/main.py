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

def memoize(
    f: Callable[[State, Player,int], tuple[Score, Action]]
) -> Callable[[State, Player,int], tuple[Score, Action]]:
    
    # max in cache 1000 ?
    
    cache = {} # closure

    # ajouter de la symétrie ?
    # principe on tourne la grille 3 fois pour voir si cette grille n'est pas présente en cache

    def g(state: State, player: Player,depth:int):
        
        state_inverted : State = (state[2],state[1],state[0])
        state_right_tmp : list[list] = [[],[],[]]
        state_left_tmp : list[list] = [[],[],[]]
        state_vert_tmp : list[list] = [[],[],[]]

        ren : int = len(state)
        for i in range(ren):
            for j in range(ren):
                state_right_tmp[j].append(state[i][j])
                state_left_tmp[j].append(state[ren-1-i][j])
                state_vert_tmp[i].append(state[i][ren-1-j])

        
        state_vert : State = grid_list_to_grid_tuple(state_vert_tmp)
        state_right : State = grid_list_to_grid_tuple(state_right_tmp)
        state_left : State = grid_list_to_grid_tuple(state_left_tmp)

        if state in cache:
            return cache[state]
        elif state_inverted in cache:
            returned = cache[state_inverted]
            value : list[int] = [returned[1][0],returned[1][1]]
            if value[0] == 2:
                value[0] = 0
            elif value[0] == 0:
                value[0] = 2
            
            tup : Action = (value[0],value[1])
            return (returned[0],tup)

        elif state_left in cache:
            returned = cache[state_left]
            value : list[int] = [returned[1][0],returned[1][1]]
            final : list[int] = []
            if value[1] == 2:
                final.append(0)
            elif value[1] == 0:
                final.append(2)
            else:
                final.append(1)
            final.append(value[0])

            tup : Action = (final[0],final[1])

            return (returned[0],tup)

        elif state_right in cache:
            returned = cache[state_right]
            value : list[int] = [returned[1][0],returned[1][1]]
            tup : Action = (value[1],value[0])
            return (returned[0],tup)

        elif state_vert in cache:

            returned = cache[state_vert]
            value : list[int] = [returned[1][0],returned[1][1]]
            if value[1] == 2:
                value[1] = 0
            elif value[1] == 0:
                value[1] = 2
            return (returned[0],(value[0],value[1]))


        val = f(state, player,depth)
        cache[state] = val
        return val
    return g


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
    return (
        (grid[0][0], grid[0][1], grid[0][2]),
        (grid[1][0], grid[1][1], grid[1][2]),
        (grid[2][0], grid[2][1], grid[2][2]),
    )


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


def score(grid: State, player: Player) -> float:
    """returns score"""
    if not line(grid, 1) and not line(grid, 2):
        return 0
    if line(grid, player):
        return 1
    return -1


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
                actions.append((i, j))
    return actions


def play(grid: State, player: Player, action: Action) -> State:
    """effectuer une action si elle est possible"""
    my_grid = grid_tuple_to_grid_list(grid)
    if action in legals(grid):
        my_grid[action[0]][action[1]] = player
        return grid_list_to_grid_tuple(my_grid)

    raise ValueError("action impossible")


def input_to_action(my_input: int) -> Action:
    """convert input to action"""
    col = my_input % 3
    l = math.floor(my_input / 3)
    action: Action = (l, col)
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
    choice: Action = legals_choices[0]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice


def strategy_random(grid: State, player: Player) -> Action:
    """strategy random choice"""
    legals_choices: list[Action] = legals(grid)
    nb: int = random.randint(0, len(legals_choices) - 1)
    choice: Action = legals_choices[nb]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice


# ========================== MIN MAX ==========================
def minmax(grid: State, player: Player) -> float:
    """basic min max"""
    player1: Player = 1
    player2: Player = 2
    possibilities: list[Action]
    best: float
    if final(grid):
        return score(grid, player1)

    if player == 1:  # maximazing player
        best = float("-inf")
        possibilities = legals(grid)
        print("joueur1", possibilities)
        for item in possibilities:
            tmp = play(grid, player, item)
            val = minmax(tmp, player2)
            if max(best, val) == val:
                best = val
        return best

    if player == 2:  # minimizing player
        best = float("inf")
        possibilities = legals(grid)
        print("joueur2", possibilities)
        for item in possibilities:
            tmp = play(grid, player, item)
            val = minmax(tmp, player1)
            if min(best, val) == val:
                best = val
        return best

    raise ValueError("erreur pas de joeur connu")


# ========================== MIN MAX AVEC DEPTH ==========================
@memoize
def minmax_action(grid: State, player: Player, depth: int = 0) -> tuple[float, Action]:
    """explore possibilities"""

    player1: Player = 1
    player2: Player = 2
    best: tuple[float, Action]

    if depth == 0 or final(grid):
        return (score(grid, player1), (-1, -1))

    if player == 1:  # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = minmax_action(tmp, player2, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = minmax_action(tmp, player1, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
        return best
    raise ValueError("erreur pas de joeur connu")


def strategy_minmax(grid: State, player: Player) -> Action:
    """strategy with min max evaluation"""
    choice: Action = minmax_action(grid, player, 9)[1]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice


# ========================== MIN MAX RANDOM ==========================
def minmax_actions(
    grid: State, player: Player, depth: int = 0
) -> tuple[float, list[Action]]:
    """indeterminist min-max"""
    player1: Player = 1
    player2: Player = 2
    tab: list[Action] = []
    best: tuple[float, list[Action]]
    if depth == 0 or final(grid):
        return (score(grid, player1), [])

    if player == 1:  # maximazing player
        best = (float("-inf"), [])
        tab = []
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = minmax_actions(tmp, player2, depth - 1)
            if (
                max(best[0], returned_values[0]) == returned_values[0]
                or returned_values[0] == best[0]
            ):
                if depth == 9:
                    if returned_values[0] != best[0]:
                        tab = []
                    tab.append(item)
                    best = (returned_values[0], tab)
                best = (returned_values[0], tab)
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), [])
        tab = []
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = minmax_actions(tmp, player1, depth - 1)
            if (
                min(best[0], returned_values[0]) == returned_values[0]
                or returned_values[0] == best[0]
            ):
                if depth == 9:
                    if returned_values[0] != best[0]:
                        tab = []
                    tab.append(item)
                    best = (returned_values[0], tab)
                best = (returned_values[0], tab)
        return best
    raise ValueError("erreur pas de joeur connu")


def strategy_minmax_random(grid: State, player: Player) -> Action:
    """strategy with min max evaluation"""
    returned_values: tuple[float, list[Action]] = minmax_actions(grid, player, 9)
    nb: int = random.randint(0, len(returned_values[1]) - 1)
    choice: Action = returned_values[1][nb]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice


# ========================== ALPHA BETA ==========================
def alpha_beta(
    grid: State, player: Player, alpha: float, beta: float, depth: int = 0
) -> tuple[float, Action]:
    """explore possibilities"""

    player1: Player = 1
    player2: Player = 2
    best: tuple[float, Action]
    b : float = beta
    a : float = alpha

    if depth == 0 or final(grid):
        return (score(grid, player1), (-1, -1))

    if player == 1:  # maximazing player
        best = (float("-inf"), (-1, -1))
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = alpha_beta(tmp, player2, a, b, depth - 1)
            if max(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            a = max(a, best[0])
            if a >= b:
                break
        return best

    if player == 2:  # minimizing player
        best = (float("inf"), (-1, -1))
        for item in legals(grid):
            tmp = play(grid, player, item)
            returned_values = alpha_beta(tmp, player1, a, b, depth - 1)
            if min(best[0], returned_values[0]) == returned_values[0]:
                best = (returned_values[0], item)
            b = min(b, best[0])
            if a >= b:
                break
        return best

    raise ValueError("erreur pas de joeur connu")

def strategy_alphabeta(grid: State, player: Player) -> Action:
    """strategy with alpha evaluation"""
    choice: Action = alpha_beta(grid, player, float("-inf"), float("inf"), 9)[1]
    print(f"\nChoix du joueur {player} : {choice}")
    return choice

# ========================== JEU PRINCIPAL ==========================
def tictactoe(strategy_x: Strategy, strategy_o: Strategy, debug: bool = False) -> Score:
    """main game function"""
    grid: State = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    player1: Player = 1
    player2: Player = 2
    current: Player = 1
    action: Action
    while final(grid) == debug:
        if current == player1:
            action = strategy_x(grid, player1)
            try:
                grid = play(grid, player1, action)
            except ValueError:
                #clear()
                print(
                    "\n\nAction impossible, la case est déjà prise, retentez votre coup"
                )
                time.sleep(1.5)
                current = 2  # permet de ne pas changer de joueur à l'exception
        else:
            action = strategy_o(grid, player2)
            try:
                grid = play(grid, player2, action)
            except ValueError:
                #clear()
                print(
                    "\n\nAction impossible, la case est déjà prise, retentez votre coup"
                )
                time.sleep(1.5)
                current = 1  # permet de ne pas changer de joueur à l'exception
        if current == player1:
            current = player2
        else:
            current = player1
    #clear()
    print("Grid State : \n")
    pprint(grid)
    if line(grid, player1):
        print("\nLe joueur1 gagne !")
    elif line(grid, player2):
        print("\nLe joueur2 gagne !")
    else:
        print("\n=============== MATCH NUL ===============")

    return score(grid, player1)


v = 0
e = 0
d = 0
start = time.time()
for i in range(10000):
    val = tictactoe(strategy_random, strategy_minmax)
    if val == 1:
        d+=1
    elif val == 0:
        e+=1
    else:
        v+=1
print("temps : ",time.time() -start)
print(f"Le joueur2 a gagné {v} fois, a fait {e} égalités et a perdu {d} fois")
