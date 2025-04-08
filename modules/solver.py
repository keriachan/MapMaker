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

def tuile_contrainte(tuiles: list[dict], grille: list[list[str]]) -> tuple | None:
    min_taille = None
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j)
                if min_taille is None or len(tuiles_possibles) < min_taille:
                    contrainte = (i, j, tuiles_possibles)
                    min_taille = len(tuiles_possibles)
    return contrainte

def grille_tuple(grille: list[list[str]]) -> tuple:
    return tuple(tuple(tuiles) for tuiles in grille)

def solver_profondeur(grille: list[list[str]], tuiles: list[dict]) -> bool:
    if grille_remplie(grille):
        return True
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j)
                if len(tuiles_possibles) == 0:
                    return False
                random.shuffle(tuiles_possibles)
                for tuile in tuiles_possibles:
                    grille[i][j] = tuile["nom"]
                    if solver_profondeur(grille, tuiles):
                        return True
                    grille[i][j] = None
    return False

def solver_profondeur_contrainte(grille: list[list[str]], tuiles: list[dict]) -> bool:
    if grille_remplie(grille):
        return True
    i, j, tuiles_possibles = tuile_contrainte(tuiles, grille)
    if len(tuiles_possibles) == 0:
        return False
    random.shuffle(tuiles_possibles)
    for tuile in tuiles_possibles:
        grille[i][j] = tuile["nom"]
        if solver_profondeur_contrainte(grille, tuiles):
            return True
        grille[i][j] = None
    return False



def solver_largeur(grille: list[list[str]], tuiles: list[dict]) -> bool:
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
                        tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, current_grille, i, j)
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