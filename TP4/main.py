""" IA02 TP4 - TicTacToe"""

from typing import Callable

# Defined types
Grid = tuple[tuple[int, ...], ...]
State = Grid
Action = tuple[int, int]
Player = int
Score = float
Strategy = Callable[[Grid, Player], Action]

# Defined constants
DRAW = 0
EMPTY = 0
X = 1
O = 2



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
    return line(grid, 1) or line(grid,2)

def score(grid: State) -> float:
    """returns score"""



def pprint(grid: State):
    """prints grid"""
    for line in grid:
        for item in line:
            if item == 0:
                print("*", end=" ")
            elif item == 1:
                print("X", end=" ")
            elif item == 2:
                print("O", end=" ")
            else : 
                raise("Erreur de données dans la grille")
        print()

def legals(grid: State) -> list[Action]:
    """returns available actions"""
    actions : list[Action] = []
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                actions.append([i,j])
    return actions



def play(grid: State, player: Player, action: Action) -> State:
    """effectuer une action si elle est possible """
    my_grid = grid_tuple_to_grid_list(grid)
    if list(action) in legals(grid):
        my_grid[action[0]][action[1]] = player
        return grid_list_to_grid_tuple(my_grid)
    else: 
        raise("action impossible")
    return grid


def strategy_brain(grid: Grid, player: Player) -> Action:
    print("à vous de jouer: ", end="")
    s = input()
    print()
    t = ast.literal_eval(s)

    return t
 Comment
 Suggest edit



tab = ((0,1,1),(0,1,0),(0,2,1))

pprint(tab)
tab = play(tab, 2, (0,1))
print("\n")
pprint(tab)



