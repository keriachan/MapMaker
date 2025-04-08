from modules import gestion_tuiles
import random

def grille_remplie(grille: list[list[str]]):
    for ligne in grille:
        for tuile in ligne:
            if tuile is None:
                return False
    return True

def solver_nul(grille: list[list[str]], tuiles: list[dict]) -> bool:
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
                    if solver_nul(grille, tuiles):
                        return True
                    grille[i][j] = None
    return False