def emplacement_valide(grille: list[list[str]], i: int, j: int, nom_tuile: str, riviere: bool = False) -> bool:
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
    if riviere:
        return riviere_valide(grille, i, j, nom_tuile)   
    return True

def riviere_valide(grille, i, j, nom_tuile):
    if not "R" in nom_tuile:
        return True
    cote = []
    visite = {(i, j)}
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    indices_R = [k for k, c in enumerate(nom_tuile) if c == 'R']
    if "M" in nom_tuile:
            cote.append("M")
    for c in nom_tuile: #Mer/bord
        if c in ["S", "D", "H", "G", "B"]:
            cote.append("S")
            break
    for k in range(len(indices_R)):
        dx, dy = direction[indices_R[k]]
        x, y = i + dx, j + dy
        cote_temp, visite = parcours_riviere(grille, x, y, visite)
        cote.append(cote_temp)
    if False in cote or len(cote) != len(set(cote)):
        return False
    return True

def parcours_riviere(grille, i, j, visite) -> tuple[str, set]:
    if (i, j) in visite: #boucle ou retour en arriere
        return False, visite
    visite.add((i, j))
    
    if i < 0 or i >= len(grille) or j < 0 or j >= len(grille[0]) or grille[i][j] is None: #hors map ou pas de tuile
        return "vide", visite
    
    elif "M" in  grille[i][j]: #Montagne
        return "M", visite
    
    for c in grille[i][j]: #Mer/bord
        if c in ["S", "D", "H", "G", "B"]:
            return "S", visite
    
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    indices_R = [k for k, c in enumerate(grille[i][j]) if c == 'R']
    for k in range(len(indices_R)):
        dx, dy = direction[indices_R[k]]
        x, y = i + dx, j + dy
        cote, visite = parcours_riviere(grille, x, y, visite)
        if cote is False:
            continue
        else:
            return cote, visite

def tuiles_possibles(tuiles: list[dict], grille: list[list[str]], i: int, j: int, riviere: bool = False) -> list[dict]:
    return [tuile for tuile in tuiles if emplacement_valide(grille, i, j, tuile["nom"], riviere)]