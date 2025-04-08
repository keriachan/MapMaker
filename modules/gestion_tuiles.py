



def rivieres(grille,i,j, nom_tuile, h = {}):
    for k in range(len(nom_tuile)):
        if nom_tuile[k] == "R":
            break
        elif k == 3:
            return True
    
    direction = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)]
    t_true = [False]*4
    for dx, dy, l in direction:
        x, y = i + dx, j + dy
        if 0 <= x < len(grille) and 0 <= y < len(grille[0]):
            if (x,y) in list(h.keys()):
                if l == (h[(x,y)] + 2) % 4:
                    continue
                else:
                    return False
            if nom_tuile[l] == "R":
                    if grille[x][y] is not None:
                        h[(x,y)] = l
                        t_true[l] == rivieres(grille,x,y, grille[x][y], h = h)

                
        

def emplacement_valide(grille: list[list[str]], i: int, j: int, nom_tuile: str):
    direction = [(-1, 0, 0), (0, 1, 1), (1, 0, 2), (0, -1, 3)] #(x, y, indice de la lettre a comparer)
    error = 0
    for dx, dy, l in direction:
        x, y = i + dx, j + dy
        if 0 <= x < len(grille) and 0 <= y < len(grille[0]):
            if grille[x][y] is None:
                continue
            elif grille[x][y][(l + 2)%4] != nom_tuile[l]:
                return False
        else:
            error += 1
    if error == 4:
        return False
    return True

def tuiles_possibles(tuiles: list[dict], grille: list[list[str]], i: int, j: int):
    return [tuile for tuile in tuiles if emplacement_valide(grille, i, j, tuile["nom"])]