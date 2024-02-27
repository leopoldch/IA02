from typing import List, Dict, Generator
import time
import statistics

def decomp(n: int, nb_bits: int) -> List[bool]:
    list :List[bool] = []
    list_temp : List[bool] = []
    tmp :str = bin(n)
    tmp = tmp[2:]
    for i in range(len(tmp)):
        list_temp.append(bool(int(tmp[i])))   
    for i in range(nb_bits-len(tmp)):
        list.append(False)
    list += list_temp

    return list 

def interpretation(voc: List[str], vals: List[bool]) -> Dict[str, bool]:
    returned_dict : Dict[str, bool] = {}
    if len(voc) != len(vals):
        raise Exception("Chaque varaible doit être lié à une interpretation")
    for i in range(len(voc)):
        returned_dict[voc[i]] = vals[i]
    return returned_dict
        
def gen_interpretations(voc: List[str]) -> Generator[Dict[str, bool], None, None]:
    for i in range(2**len(voc)):
        values : List[bool] = decomp(i, len(voc))
        to_append : Dict[str,bool] = {}
        for k in range(len(voc)):
            to_append[voc[k-1]]=values[k-1]   
        yield to_append
    
def valuate(formula: str, interpretation: Dict[str, bool]) -> bool:
    string : str = formula
    temp : str = formula.replace("not", "").replace("(","").replace(")", "").replace("and", "").replace("or", "").replace("==","")
    var : List[str] = temp.split("  ")
    for v in var:
        tmp_bool : str = str(interpretation[v])
        string = string.replace(v, tmp_bool, 1)

    return eval(string)

def table(formula: str, interpretation: Dict[str, bool]) -> None:

    var : List[str] = []
    for key in interpretation:
        var.append(key)
    # Affichage 
    print("+", end="")
    for i in range(len(interpretation)):
        print("---+", end="")
    print("-------+")    
    print("|", end="")
    for v in var:
        print(f" {v} |", end="")
    print(" eval. |")    
    print("+", end="")
    for i in range(len(interpretation)):
        print("---+", end="")
    print("-------+")    
    # Fin de l'affichage du début 
    
    all_interps = gen_interpretations(var)
    for i in range(2**len(var)):
        tab : Dict[str, bool] = next(all_interps)
        print(f"| {switchl(tab['A'])} | {switchl(tab['B'])} | {switchl(tab['C'])} |", end="")
        print(f"   {switchl(valuate(formula, tab))}   |")

    #affichage de fin : 
    print("+", end="")
    for i in range(len(interpretation)):
        print("---+", end="")
    print("-------+")      

def switchl(state : bool) -> str:
    if state == False:
        return 'F'
    else:
        return 'T'

def isValid(formula: str) -> bool:
    # récuérations des variables : 
    temp : str = formula.replace("not", "").replace("(","").replace(")", "").replace("and", "").replace("or", "").replace("==","")
    var : List[str] = temp.split("  ")
    all_interps = gen_interpretations(var)
    for i in range(2**len(var)):
        tab : Dict[str, bool] = next(all_interps)
        if(not valuate(formula, tab)):
            return False
    return True    

def isContradictory(formula: str) -> bool:
    temp : str = formula.replace("not", "").replace("(","").replace(")", "").replace("and", "").replace("or", "").replace("==","")
    var : List[str] = temp.split("  ")
    all_interps = gen_interpretations(var)
    for i in range(2**len(var)):
        tab : Dict[str, bool] = next(all_interps)
        if(valuate(formula, tab)):
            return False
    return True   

def isContingent(formula: str) -> bool:
    if(not isValid(formula) and not isContradictory(formula)):
        return True
    return False   

def verif(formula: str) -> str:
    if isValid(formula):
        return "Valide"
    elif isContradictory(formula):
        return "Contradictoire"
    else:
        return "Contingent"

def validationTest():
    start = time.time()
    myformula : str = "A"
    for i in range(22):
        var : str = "A" + str(i+1)
        myformula += " and " + var

    result : str = verif(myformula)
    end = time.time()
    print(f"Temps d\'exécution : {end - start}secondes")
    print(f"\nRésultat du calcul : {result}")







#for i in range(8):
#    print(decomp(i,3))

#print("\n\n\n")
#g = gen_interpretations(["A", "B", "C"])
#for i in range(8):
#    print(next(g))


#for i in gen_interpretations(["toto", "tutu"]):
#    print(i)
        

#table("(A or B) and not(C)", ["A", "B", "C"])

validationTest();