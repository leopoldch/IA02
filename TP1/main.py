from typing import List, Dict, Generator
import time


def decomp(n: int, nb_bits: int) -> List[bool]:
    my_list: List[bool] = []
    list_temp: List[bool] = []
    tmp: str = bin(n)
    tmp = tmp[2:]
    for var in tmp:
        list_temp.append(bool(int(var)))
    for _ in range(nb_bits - len(tmp)):
        my_list.append(False)
    my_list += list_temp

    return my_list


def interpretation(voc: List[str], vals: List[bool]) -> Dict[str, bool]:
    returned_dict: Dict[str, bool] = {}
    if len(voc) != len(vals):
        raise Exception("Chaque varaible doit être lié à une interpretation")
    for val1, val2 in zip(voc, vals):
        returned_dict[val1] = val2
    return returned_dict


def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None]:
    for i in range(2 ** len(voc)):
        values: List[bool] = decomp(i, len(voc))
        yield interpretation(voc, values)


def valuate(formula: str, interps: Dict[str, bool]) -> bool:
    return eval(formula, interps)


def table(formula: str, interps: Dict[str, bool]) -> None:

    var: List[str] = []
    for key in interps:
        var.append(key)
    # Affichage
    print("+", end="")
    for _ in enumerate(interps):
        print("---+", end="")
    print("-------+")
    print("|", end="")
    for v in var:
        print(f" {v} |", end="")
    print(" eval. |")
    print("+", end="")
    for _ in enumerate(interps):
        print("---+", end="")
    print("-------+")
    # Fin de l'affichage du début
    for interps_val in gen_interpretations(var):
        tab: Dict[str, bool] = interps_val
        print(
            f"| {switchl(tab['A'])} | {switchl(tab['B'])} | {switchl(tab['C'])} |",
            end="",
        )
        print(f"   {switchl(valuate(formula, tab))}   |")

    # affichage de fin :
    print("+", end="")
    for _ in enumerate(interps):
        print("---+", end="")
    print("-------+")


def switchl(state: bool) -> str:
    if not state:
        return "F"
    return "T"


def is_valid(formula: str) -> bool:
    # récuérations des variables :
    temp: str = (
        formula.replace("not", "")
        .replace("(", "")
        .replace(")", "")
        .replace("and", "")
        .replace("or", "")
        .replace("==", "")
    )
    var: List[str] = temp.split("  ")
    for interps in gen_interpretations(var):
        tab: Dict[str, bool] = interps
        if not valuate(formula, tab):
            return False
    return True


def is_contradictory(formula: str) -> bool:
    temp: str = (
        formula.replace("not", "")
        .replace("(", "")
        .replace(")", "")
        .replace("and", "")
        .replace("or", "")
        .replace("==", "")
    )
    var: List[str] = temp.split("  ")
    for interps in gen_interpretations(var):
        tab: Dict[str, bool] = interps
        if valuate(formula, tab):
            return False
    return True


def is_contingent(formula: str) -> bool:
    if not is_valid(formula) and not is_contradictory(formula):
        return True
    return False


def verif(formula: str) -> str:
    if is_valid(formula):
        return "Valide"
    if is_contradictory(formula):
        return "Contradictoire"
    return "Contingent"


def validation_test():
    start = time.time()
    myformula: str = "A"
    for i in range(20):
        var: str = "A" + str(i + 1)
        myformula += " and " + var

    result: str = verif(myformula)
    end = time.time()
    print(f"Temps d'exécution : {end - start}secondes")
    print(f"\nRésultat du calcul : {result}")


def is_cons(f1: str, f2: str, voc: List[str]) -> bool:
    # on doit regarder si quand f1 est vraie f2 est vraie aussi !
    # on suppose que les deux experssions ont les mêmes variables (le même vocabulaire exactement)
    for interp in gen_interpretations(voc):
        tab: Dict[str, bool] = interp
        val1: bool = valuate(f1, tab)
        val2: bool = valuate(f2, tab)
        if val1 and not val2:
            return False
    return True


def test_cons():
    print(is_cons("A or B", "A and B", ["A", "B"]))
    print(is_cons("A and B and C", "A or B or C", ["A", "B", "C"]))
    print(
    is_cons(
            "A and B and C or D",
            "A or B or C and D and not(E)",
            ["A", "B", "C", "D", "E"],
        )
    )


#print(valuate("A and not(B)", {"A":True, "B": False} ))


# for i in range(8):
#    print(decomp(i,3))

# print("\n\n\n")
# g = gen_interpretations(["A", "B", "C"])
# for i in range(8):
#    print(next(g))


# for i in gen_interpretations(["toto", "tutu"]):
#    print(i)


table("(A or B) and not(C)", ["A", "B", "C"])

# validation_test()
test_cons()
