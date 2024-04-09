"""Fichier pour résoudre un sudoku avec le solveur SAT gophersat"""

import subprocess
from itertools import combinations


class Sudoku:
    """classe qui fait office de compteur"""

    def __init__(self) -> None:
        self.__nb_clauses = 0
        self.__nb_var = 729

    def add_clause(self) -> None:
        """setter pour les clauses"""
        self.__nb_clauses += 1

    def get_clause(self) -> int:
        """getter pour les clauses"""
        return self.__nb_clauses

    def get_var(self) -> int:
        """getter pour le nombre de variables"""
        return self.__nb_var


compteur = Sudoku()


# aliases de type
Grid = list[list[int]]
PropositionnalVariable = int
Literal = int
Clause = list[Literal]
ClauseBase = list[Clause]
Model = list[Literal]

grid_example = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

grid_example_2 = [
    [4, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 1, 0, 0, 9, 6, 0, 0, 0],
    [0, 0, 3, 2, 0, 0, 6, 0, 1],
    [5, 3, 1, 6, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 9, 0, 0, 0],
    [1, 8, 5, 0, 6, 0, 0, 0, 4],
    [0, 6, 2, 4, 0, 5, 0, 7, 0],
    [0, 0, 0, 9, 0, 0, 0, 0, 0],
]

grid_hard = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 9, 6, 0, 0, 0],
    [0, 0, 3, 2, 0, 0, 6, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 9, 0, 0, 0],
    [1, 0, 0, 0, 6, 0, 0, 0, 4],
    [0, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def cell_to_variable(i: int, j: int, val: int) -> int:
    """passage d'une case à une valeur"""
    line = (i) * 81
    col = (j) * 9
    return line + col + val + 1


def variable_to_cell(value: int) -> tuple[int, int, int]:
    """passage d'une valeur à une case"""
    v: int = value - 1
    returned_value: int = v % 9
    col: int = (v // 9) % 9
    line: int = v // 81
    return (line, col, returned_value)


def model_to_grid(model: Model, nb_vals: int = 9) -> Grid:
    """passer d'un modèle à une grid"""
    main_tab = [[] for _ in range(nb_vals)]
    for var in model:
        if var != 0:
            cell: tuple = variable_to_cell(var)
            main_tab[cell[0]].append(cell[2] + 1)
    return main_tab


def unique(variables: list) -> list:
    """contrainte d'unicité"""
    clauses: list = []
    clauses.append(variables)
    comb: list = list(combinations(variables, 2))
    for item in comb:
        clauses.append([-item[0], -item[1]])
    return clauses


def clauses_to_dimacs(tab: list) -> str:
    """Fonction qui permet de générer les clauses grâce à un tableau facilement"""
    mystr: str = ""
    for item in tab:
        mystr += f"{item} "
    mystr += "0"
    compteur.add_clause()
    return mystr


def create_line_constraints() -> str:
    """créer les contraintes pour les lignes"""

    mystr: str = ""
    for line in range(9):
        for val in range(9):
            values: list = []
            for col in range(9):
                value: int = cell_to_variable(line, col, val)
                values.append(value)
            clauses: list = unique(values)
            for item in clauses:
                mystr += clauses_to_dimacs(item) + "\n"
    return mystr


def create_column_constraints() -> str:
    """créer les contraintes pour les colones"""

    mystr: str = ""
    for col in range(9):
        for val in range(9):
            values: list = []
            for line in range(9):
                value: int = cell_to_variable(line, col, val)
                values.append(value)
            clauses: list = unique(values)
            for item in clauses:
                mystr += clauses_to_dimacs(item) + "\n"
    return mystr


def create_box_constraints() -> str:
    """créer les contraintes pour les box"""
    mystr: str = ""
    for val in range(9):
        # on doit faire les contraintes pour
        # toutes les variables possibles

        for box_line in range(3):
            for box_col in range(3):
                cells: list = []
                for line in range(3):
                    for col in range(3):
                        cells.append(
                            cell_to_variable(
                                line + box_line * 3, col + box_col * 3, val
                            )
                        )
                for item in unique(cells):
                    mystr += clauses_to_dimacs(item) + "\n"
    return mystr


def create_value_constraints(grid: Grid):
    """rajouter les contraintes sur les variables déjà connues"""
    mystr: str = ""
    for line in range(9):
        for col in range(9):
            if grid[line][col] != 0:
                cell = cell_to_variable(line, col, grid[line][col] - 1)
                mystr += f"{cell} 0\n"
    return mystr


def create_variables_constraints() -> str:
    """créer les contraintes pour les variables"""
    mystr: str = ""
    for col in range(9):
        for line in range(9):
            values: list = []
            for val in range(9):
                value: int = cell_to_variable(line, col, val)
                values.append(value)
            clauses: list = unique(values)
            for item in clauses:
                mystr += clauses_to_dimacs(item) + "\n"
    return mystr


def make_begin_file(nb_var: int, nb_clauses: int, filename: str) -> str:
    """génération de l'entete"""
    my_line: str = ""
    my_line += f"c FILE: {filename}\n"
    my_line += "c \n"
    my_line += "c SOURCE: Léopold Chappuis (leopold.chappuis@etu.utc.fr),\n"
    my_line += "c \n"
    my_line += "c DESCRIPTION: SAT solver Graph \n"
    my_line += "c \n"
    my_line += "c NOTE: Satisfiable \n"
    my_line += "c \n"
    my_line += f"p cnf {nb_var} {nb_clauses}\n"
    return my_line


def write_dimacs_file(dimacs: str, filename: str):
    """écriture dans le fichier"""
    with open(filename, "w", encoding="utf8") as file:
        file.write(dimacs)


def generate_problem(grid: Grid):
    """fonction principale"""
    filename: str = "sudoku.cnf"
    constraints: str = ""
    tmp: str = ""
    tmp += create_column_constraints()
    tmp += create_line_constraints()
    tmp += create_box_constraints()
    tmp += create_variables_constraints()
    tmp += create_value_constraints(grid)
    constraints += make_begin_file(compteur.get_var(), compteur.get_clause(), filename)
    constraints += tmp

    write_dimacs_file(constraints, filename)


def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> tuple[bool, list[int]]:
    """fonction pour run le solver"""
    process = subprocess.run(
        f"/Users/leo/go/bin/{cmd} {filename}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        encoding=encoding,
    )

    returned_values: str = process.stdout
    vals: list = returned_values.split("\n")
    verif: str = vals[1]
    if verif == "s UNSATISFIABLE":
        return (False, [])

    numbers: list[int] = []
    vals = vals[2]
    vals = vals.split(" ")
    vals.pop(0)
    vals.pop(len(vals) - 1)
    for item in vals:
        if int(item) > 0:
            numbers.append(int(item))
    return (True, numbers)


def print_grid(grid: Grid):
    """permet d'afficher une grille facilement"""
    my_str: str = ""
    for line in range(9):
        my_str += "-------------------------\n"
        my_str += "| "
        for col in range(9):
            number: int = grid[line][col]
            if number == 0:
                my_str += ". "
            else:
                my_str += f"{number} "
            if col in [2, 5, 8]:
                my_str += "| "
            if col == 8:
                my_str += "\n"
    my_str += "-------------------------\n"
    print(my_str)


def resolve(grid: Grid, filename: str):
    """fonction principale"""
    generate_problem(grid)
    response: tuple = exec_gophersat(filename)

    if response[0]:
        variables: Model = response[1]
        final_grid: Grid = model_to_grid(variables)
        print("Problème initial : ")
        print_grid(grid)
        print("\n")
        print("Problème résolu : ")
        print_grid(final_grid)
    else:
        print("Non solvable.")
    print(
        "Voulez vous connaitre le nombre de models trouvés ?\
            \nCette opération peut être longue", end=" "
    )
    verif = ""
    while verif.lower() not in ["y", "n"]:
        verif = str(input("[y/n]"))
    if verif.lower() == "y":
        nb_models = count_gophersat(filename)
        print(f"Nombre de models : {nb_models}")
    print("\nFin du programme")


def count_gophersat(
    filename: str, cmd: str = "gophersat --count", encoding: str = "utf8"
) -> tuple[bool, list[int]]:
    """fonction pour run le solver"""
    process = subprocess.run(
        f"/Users/leo/go/bin/{cmd} {filename}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        encoding=encoding,
    )

    returned_values: str = process.stdout
    tab: list[str] = returned_values.split("\n")
    returned_values = tab[1]
    return returned_values


resolve(grid_example_2, "sudoku.cnf")
