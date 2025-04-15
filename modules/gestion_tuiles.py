



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
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    error = 0
    for l, (dx, dy) in enumerate(direction):
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
    
    #if not riviere_valide(grille, i, j, nom_tuile):
    #   return False   
    return True

def riviere_valide(grille, i, j, nom_tuile):
    debut, fin = None, None
    if not "R" in nom_tuile:
        return True
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    indices_R = [k for k, c in enumerate(nom_tuile) if c == 'R']
    for k in range(len(indices_R)):
        dx, dy = direction[indices_R[k]]
        x, y = i + dx, j + dy
        if 0 <= x < len(grille) and 0 <= y < len(grille[0]):
            if k == 0:
                debut, visite = parcours_riviere(grille, x, y, {(i, j)}, (dx, dy))
            else:
                fin, visite = parcours_riviere(grille, x, y, visite, (dx, dy))
        else:
            return True
    print(debut, fin)
    if (debut is False or fin is False) or (debut != "vide" and debut == fin):
        return False
    return True

def parcours_riviere(grille, i, j, visite, vect) -> tuple[str, set]:
    #boucle
    if (i, j) in visite:
        return False, visite
    visite.add((i, j))
    if grille[i][j] is None:
        return "vide", visite
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    indices_R = [k for k, c in enumerate(grille[i][j]) if c == 'R']
    for k in range(len(indices_R)):
        dx, dy = direction[indices_R[k]]
        x, y = i + dx, j + dy
        if 0 <= x < len(grille) and 0 <= y < len(grille[0]):
            if (dx, dy) == (vect[0] * -1, vect[1] * -1):#opposé
                continue
            #vide ou riviere
            if grille[x][y] is None or grille[x][y][(indices_R[k]+2)%4] == "R":
                return parcours_riviere(grille, x, y, visite)
            #montagne ou mer
            elif grille[x][y][(indices_R[k]+2)%4] == "M" or grille[x][y][(indices_R[k]+2)%4] == "S":
                return grille[x][y][(indices_R[k]+2)%4], visite
            else:
                return False, visite
        else:
            return "vide", visite
    
def tuiles_possibles(tuiles: list[dict], grille: list[list[str]], i: int, j: int):
    return [tuile for tuile in tuiles if emplacement_valide(grille, i, j, tuile["nom"])]