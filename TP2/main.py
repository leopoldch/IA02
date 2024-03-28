"""Code du TP2 IA02"""

import os
import math
import subprocess
import networkx as nx
import matplotlib.pyplot as plt

# première partie du TP tester gospherat sur les exemples :


def exo1() -> None:
    """Function solving exercice 1."""

    dossier: str = "/Users/leo/Documents/UTC/IA02/TP2/examples"

    # Parcourir tous les fichiers dans le dossier
    for file in os.listdir(dossier):
        # Construire le chemin complet du fichier
        path = os.path.join(dossier, file)

        # Exécuter la commande 'ls' sur le fichier
        # Notez que 'ls' est une commande Unix/Linux. Pour Windows, vous pouvez utiliser 'dir'
        # Pour rendre le code compatible avec Windows, vous pouvez utiliser 'dir' à la place de 'ls'
        # et ajouter '/b' pour une sortie plus simple
        commande = f"/Users/leo/go/bin/gophersat {path}"
        process = subprocess.run(
            commande,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )

        # Afficher la sortie de la commande 'ls'
        print(f"résultat pour  {file} :")
        print(process.stdout)
        print("-----------------------------")

    # Afficher les erreurs éventuelles
    if process.stderr:
        print("Erreurs :")
        print(process.stderr)


## exo 2 modélisation cohérante car satisfiable par le solveur
#  My -> -Mo
#  -My -> Mam & Mo
#  -Mam & -Mo -> Co
#  Co -> Mag
# Sous CNF
# noms des variables
# 1 <-> my
# 2 <-> mo
# 3 <-> mam
# 4 <-> co
# 5 <-> mag

# modifier le fichier CNF en ajoutant un clause pour arriver à l'absurde


# Exo3


# On doit donner une graphe en entrée; Stocker


# exemple de graphe

graph1: list = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (1, 6),
    (6, 9),
    (6, 8),
    (2, 7),
    (7, 10),
    (7, 9),
    (3, 8),
    (8, 10),
    (4, 9),
    (5, 10),
    (1, 5),
]


def color_graph(graph: list) -> None:
    """cette fonction doit retourner la str sous format DIMACS"""
    my_line = ""
    my_line += "c FILE: graph_gen.cnf\n"
    my_line += "c \n"
    my_line += "c SOURCE: Léopold Chappuis (leopold.chappuis@etu.utc.fr),\n"
    my_line += "c \n"
    my_line += "c DESCRIPTION: SAT solver Graph \n"
    my_line += "c \n"
    my_line += "c NOTE: Satisfiable \n"
    my_line += "c \n"
    sommets = []
    for elem in graph:
        if elem[0] not in sommets:
            sommets.append(elem[0])
        if elem[1] not in sommets:
            sommets.append(elem[1])

    # nombre de sommets par rapport aux couleurs
    # 1 -> sommet 1 R /  2 -> sommet 1 G / 3 -> sommet 1 B
    # sommet = int(nb / 3)

    nb_var = len(sommets) * 3
    nb_lines = 0

    temp = ""
    for i in range(1, nb_var + 1, 3):
        temp += f"{i} {i+1} {i+2} 0\n"
        temp += f"-{i} -{i+1} 0 \n"
        temp += f"-{i} -{i+2} 0 \n"
        temp += f"-{i+1} -{i+2} 0 \n"
        nb_lines += 4

    # maintenant il reste plus qu'à ajouter les contraintes sur les connexions
    for tup in graph:
        temp += f"-{tup[0]*3-2%3} -{tup[1]*3-2%3} 0\n"
        temp += f"-{tup[0]*3-1%3} -{tup[1]*3-1%3} 0\n"
        temp += f"-{tup[0]*3} -{tup[1]*3} 0\n"
        nb_lines += 3

    my_line += f"p cnf {nb_var} {nb_lines}\n"
    my_line += temp

    with open("graph_gen.cnf", "w", encoding="utf8") as file:
        file.write(my_line)


def print_graph(graph: list, path: str) -> None:
    """Affichage du graphe coloré"""
    pos = {
        1: (4, 5),
        2: (8, 3),
        3: (7, 0),
        4: (1, 0),
        5: (0, 3),
        6: (4, 4),
        7: (6, 2),
        8: (5, 1),
        9: (3, 1),
        10: (2, 2),
    }

    colors: dict = {0: "lightcoral", 1: "palegreen", 2: "skyblue"}
    process = subprocess.run(
        f"/Users/leo/go/bin/gophersat {path}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )

    returned_values: str = process.stdout
    temp: list = returned_values.split("\n")
    results = temp[2].replace("v", "").split(" ")
    results.remove("")
    results.pop(len(results) - 1)
    sommets_colors = {}
    for item in results:
        number = int(item)
        if number > 0:
            sommet: int = math.ceil(number / 3)
            color: str = colors[int(number % 3)]
            sommets_colors[sommet] = color
    displayed_graph = nx.Graph()

    for sommet in sommets_colors:
        displayed_graph.add_node(sommet)
    for tup in graph:
        displayed_graph.add_edge(tup[0], tup[1])
    nx.draw(
        displayed_graph,
        with_labels=True,
        pos=pos,
        node_size=500,
        node_color=list(sommets_colors.values()),
    )

    plt.show()


# exo1()

color_graph(graph1)
print_graph(graph1, "/Users/leo/Documents/UTC/IA02/TP2/graph_gen.cnf")
