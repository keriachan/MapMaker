from modules import reader

def emplacement_valide(grille: list[list[str]], i: int, j: int, nom_tuile: str, tuiles, riviere: bool = False, mer: bool = False) -> bool:
    """Determine si la tuile nom_tuile peut être placée à la position (i, j) de la grille.

    Args:
        grille (list[list[str]]): grille de jeu
        i (int): ordonnée de la tuile à placer
        j (int): abscisse de la tuile à placer
        nom_tuile (str): nom de la tuile à placer
        riviere (bool, optional): contrainte de riviere activé ou non

    Returns:
        bool: True si la tuile peut être placée, False sinon.
    """
    if mer:
        verif = False
        for c in nom_tuile: #Mer/bord
            if c in ["S", "D", "H", "G", "B"]:
                verif = True
        if not verif:
            return False
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
        return riviere_valide(grille, i, j, nom_tuile, tuiles)   
    return True

def riviere_valide(grille, i, j, nom_tuile, tuiles):
    """Vérifie si la tuile à la position (i, j) respecte les contraintes de rivière.

    Args:
        grille (list[list[str]]): grille de jeu
        i (int): ordonnée de la tuile à placer
        j (int): abscisse de la tuile à placer
        nom_tuile (str): nom de la tuile à placer

    Returns:
        bool: True si la tuile respecte les contraintes de rivière, False sinon.
    """
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
        cote_temp, visite = parcours_riviere(grille, x, y, visite, tuiles)
        cote.append(cote_temp)
    if False in cote or len(cote) != len(set(cote)):
        return False
    return True

def parcours_riviere(grille, i, j, visite, tuiles) -> tuple[str, set]:
    """Parcours de la rivière à partir de la position (i, j) dans la grille.

    Args:
        grille (list[list[str]]): grille de jeu
        i (int): ordonnée de la tuile à placer
        j (int): abscisse de la tuile à placer
        visite (set): ensemble des positions déjà visitées

    Returns:
        tuple[str, set]: debut ou finde la riviere, ensemble des positions déjà visitées
    """
    if (i, j) in visite: #boucle ou retour en arriere
        return False, visite
    visite.add((i, j))
    
    if 0 > i or i >= len(grille) or 0 > j or j >= len(grille[0]): #hors map ou pas de tuile
        return "vide", visite
    if grille[i][j] is None:
        if len(tuiles_possibles(tuiles, grille, i, j, tuiles, True, True)) > 0:
            return "vide", visite
        else:
            return False, visite
    
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

def tuiles_possibles(tuiles: list[dict], grille: list[list[str]], i: int, j: int, tuiles_dico, riviere: bool = False, mer: bool = False) -> list[dict]:
    """Renvoie la liste des tuiles qui peuvent être placées à la position (i, j) de la grille.

    Args:
        tuiles (list[dict]): liste de toutes les tuiles disponibles
        grille (list[list[str]]): grille de jeu
        i (int): ordonnée de la tuile à placer
        j (int): abscisse de la tuile à placer
        riviere (bool, optional): contrainte de riviere activé ou non

    Returns:
        list[dict]:
    """
    return [tuile for tuile in tuiles if emplacement_valide(grille, i, j, tuile["nom"], tuiles_dico, riviere, mer)]