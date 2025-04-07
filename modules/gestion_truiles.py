from modules import reader

def emplacement_valide(grille: list[list[str]], i: int, j: int, nom_tuile: str):
    direction = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)] #(x, y, indice de la lettre a comparer)
    for dx, dy, l in direction:
        x, y = i + dx, j + dy
        if 0 <= x < len(grille) and 0 <= y < len(grille[0]):
            if grille[x][y] is None:
                continue
            elif grille[x][y][(l + 2)%4] != nom_tuile[l]:
                return False
    return True

def tuiles_possibles(tuiles: list[dict], grille: list[list[str]], i: int, j: int):
    return [tuile for tuile in tuiles if emplacement_valide(grille, i, j, tuile["nom"])]