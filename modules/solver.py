from modules import gestion_tuiles
import random
from collections import deque
import copy

def grille_remplie(grille: list[list[str]]):
    for ligne in grille:
        for tuile in ligne:
            if tuile is None:
                return False
    return True

def tuile_possibilitees(tuiles: list[dict], grille: list[list[str]], liste_possibilitees: list, x, y, riviere = False) -> tuple | None:
    #premiere iteration
    if liste_possibilitees is None:
        liste_possibilitees = []
        for i in range(len(grille)):
            for j in range(len(grille[0])):
                if grille[i][j] is None:
                    tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j, riviere)
                    liste_possibilitees.append({"possibilitees": tuiles_possibles, "coord": (i, j)})
    #toutes les autres iterations
    else:
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in direction:
            i = x + dx
            j = y + dy
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is None:
                for tuile in liste_possibilitees:
                    if tuile["coord"] == (i, j):
                        tuile["possibilitees"] = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j, riviere)
                        break
    return sorted(liste_possibilitees, key=lambda x: len(x["possibilitees"]))

def grille_tuple(grille: list[list[str]]) -> tuple:
    return tuple(tuple(tuiles) for tuiles in grille)

def solver_profondeur(grille: list[list[str]], tuiles: list[dict], riviere=False) -> bool:
    if grille_remplie(grille):
        return True
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j, riviere)
                if len(tuiles_possibles) == 0:
                    return False
                random.shuffle(tuiles_possibles)
                for tuile in tuiles_possibles:
                    grille[i][j] = tuile["nom"]
                    if solver_profondeur(grille, tuiles):
                        return True
                    grille[i][j] = None
    return False

def solver_profondeur_contrainte(grille: list[list[str]], tuiles: list[dict], riviere = False, liste_possibilitees=None, x=None, y=None) -> bool:
    #cas de base
    if grille_remplie(grille):
        return True
    
    #calcule de la liste des possibilitees de tuiles pour chaque case de la grille qui a change(son voisin a ete modifie)
    liste_possibilitees = tuile_possibilitees(tuiles, grille, liste_possibilitees, x, y, riviere)
    current_tuile = liste_possibilitees[0]
    i, j = current_tuile["coord"]
    tuiles_possibles = current_tuile["possibilitees"]
    
    if len(tuiles_possibles) == 0:
        return False
    
    random.shuffle(tuiles_possibles)
    for tuile in tuiles_possibles:
        grille[i][j] = tuile["nom"]
        nouvelle_liste = liste_possibilitees[1:] #peut-etre faire une deepcopy
        if solver_profondeur_contrainte(grille, tuiles, riviere, nouvelle_liste, i, j):
            return True
        grille[i][j] = None
    return False


#trop de possibilitees, pas efficace dutout
def solver_largeur(grille: list[list[str]], tuiles: list[dict], riviere=False) -> bool:
    queue = deque()
    queue.appendleft(copy.deepcopy(grille)) #premier élément de la queue
    visite = set()

    while len(queue) > 0:
        current_grille = queue.pop()
        if grille_remplie(current_grille):
            for i in range(len(grille)):
                for j in range(len(grille[0])):
                    grille[i][j] = current_grille[i][j]
            return True
        current_grille_tuple = grille_tuple(current_grille)
        if current_grille_tuple in visite:
            continue
        else:
            visite.add(current_grille_tuple)
            for i in range(len(current_grille)):
                for j in range(len(current_grille[0])):
                    if current_grille[i][j] is None:
                        tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, current_grille, i, j, riviere)
                        random.shuffle(tuiles_possibles)
                        for tuile in tuiles_possibles:
                            nouvelle_grille = copy.deepcopy(current_grille)
                            nouvelle_grille[i][j] = tuile["nom"]
                            queue.appendleft(nouvelle_grille)
                        break
                else:
                    continue
                break
    return False