from modules import fltk, gestion_tuiles, reader, solver
import random


WIDTH, HEIGHT = 800, 800
MARGIN = WIDTH//5
NB_CASES = 10 

def convert_click_indice(x, y):#pour 10x10
    return int(y//(HEIGHT/NB_CASES)), int(x//(WIDTH/NB_CASES))

def convert_indice_click(i, j):#pour 10x10
    return int(j*(WIDTH/NB_CASES)), int(i*(HEIGHT/NB_CASES))

def champs_possibilites(tuiles_possibles_alea):
    fltk.rectangle(MARGIN, MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN, "black", "white", 2, "choices_display")
    index_tuile = 0
    for i in range(5):
        for j in range(5):
            if index_tuile > len(tuiles_possibles_alea)-1:
                break
            width_tuile, height_tuile = (WIDTH - 2*MARGIN)//5 - 2*(MARGIN//10), (HEIGHT - 2*MARGIN)//5 - 2*(MARGIN//10)
            fltk.rectangle(MARGIN + MARGIN/10 + j*(WIDTH - 2*MARGIN)/5 - 1, MARGIN + MARGIN/10 + i*(HEIGHT - 2*MARGIN)/5 - 1, MARGIN + MARGIN/10 + j*(WIDTH - 2*MARGIN)/5 + width_tuile, MARGIN + MARGIN/10 + i*(HEIGHT - 2*MARGIN)/5 + height_tuile, "black", epaisseur=1, tag="choices_display")
            fltk.image(MARGIN + MARGIN/10 + j*(WIDTH - 2*MARGIN)/5, MARGIN + MARGIN/10 + i*(HEIGHT - 2*MARGIN)/5, tuiles_possibles_alea[index_tuile]["chemin"], width_tuile, height_tuile, "nw", tuiles_possibles_alea[index_tuile]["nom"])
            index_tuile += 1

def efface_grille_displayed(grille):
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None:
                fltk.efface(grille[i][j] + f"_{i}_{j}")
                
def display_grille(grille: list[list[str]]):
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None: # peut etre faire un exept pour eviter une erreur out of ranges
                k, l = convert_indice_click(i, j)
                fltk.image(k, l, "fichiers fournis/tuiles/" + grille[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille[i][j] + f"_{i}_{j}")
   
def decale_grille_displayed(grille, dy, dx):
    """ dy, dx est le coin supérieur gauche de la grille a afficher """
    grille_temp = []
    for i in range(dy, NB_CASES + dy):
        ligne_temp = []
        for j in range(dx, NB_CASES + dx):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]):
                ligne_temp.append(grille[i][j])
            else:
                ligne_temp.append(None)
        grille_temp.append(ligne_temp)
    return grille_temp
 
def efface_2():
    fltk.efface_tout()
    fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")

def scroll_bar(taille, decale):
    max_height = HEIGHT - 2 * MARGIN
    bar_height = max_height * min(1, 25 / taille)
    y1 = MARGIN + (decale / max(1, taille - 25)) * (max_height - bar_height)
    y2 = y1 + bar_height
    fltk.rectangle(WIDTH - MARGIN - 12, y1, WIDTH - MARGIN - 2, y2, "black", "grey", 1, "scroll_bar")
    
fltk.cree_fenetre(WIDTH, HEIGHT)
fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")

grille_global = [[None] * NB_CASES for _ in range(NB_CASES)]
dx , dy = 0, 0 #coin supérieur gauche de la grille affichée par rapport à la grille globale
tuiles = reader.cree_dico("fichiers fournis/tuiles/")
choix = False
generation = True
generation_forced = False
riviere = False
decale = 0 #decale pour le scroll

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        grille_affiche = decale_grille_displayed(grille_global, dy, dx)
        if fltk.type_ev(ev) == "Quitte":
            break
        elif fltk.type_ev(ev) == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille_affiche[i][j] is not None:
                    continue
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille_affiche, i, j, riviere)
                tuiles_possibles_affiche = tuiles_possibles[:25]
                if len(tuiles_possibles) == 0:
                    print("Pas de tuiles possibles")
                    continue
                champs_possibilites(tuiles_possibles)
                scroll_bar(len(tuiles_possibles), decale)
                choix = True
            else:
                i, j = convert_click_indice(k, l)
                if tuiles_possibles is not None:
                    for tuile in tuiles_possibles_affiche:
                        if fltk.est_objet_survole(tuile["nom"]):
                            choix = False
                            fltk.efface("choices_display")
                            fltk.efface("scroll_bar")
                            for tuile_bis in tuiles_possibles_affiche:
                                fltk.efface(tuile_bis["nom"])
                            grille_global[i+dy][j+dx] = tuile["nom"]
                            fltk.image(k, l, tuile["chemin"], WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", tuile["nom"] + f"_{i}_{j}")
                            break
        elif fltk.type_ev(ev) == "ClicDroit":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille_global[i+dy][j+dx] is not None:
                        fltk.efface(grille_affiche[i][j] + f"_{i}_{j}")
                        grille_global[i+dy][j+dx] = None
        elif fltk.type_ev(ev) == "Touche":
            touche = fltk.touche(ev)
            if not choix:
                if touche == "p":#profondeur
                    generation_forced = True
                    generation = True
                    generator = solver.solver_profondeur
                    print(f"{generator.__name__} en cours...")
                elif touche == "l":#largeur trop lent
                    generation_forced = True
                    generation = True
                    generator = solver.solver_largeur
                    print(f"{generator.__name__} en cours...")
                elif touche == "c":#contrainte
                    generation_forced = True
                    generation = True
                    generator = solver.solver_profondeur_contrainte
                    print(f"{generator.__name__} en cours...")
                elif touche == "e":#efface
                    efface_2()
                    grille_global = [[None] * NB_CASES for _ in range(NB_CASES)]
                    dx, dy = 0, 0
                elif touche == "a": #arrete la generation
                    generation_forced = False
                elif touche == "m": #mer sur le bord de la grille
                    for i in range(dy, NB_CASES + dy):
                        for j in range(dx, NB_CASES + dx):
                            if i == dy or i == dy + NB_CASES - 1 or j == dx or j == dx + NB_CASES - 1:
                                k, l = convert_indice_click(i, j)
                                if grille_global[i][j] != "SSSS" and gestion_tuiles.emplacement_valide(grille_global, i, j, "SSSS"):
                                    if grille_global[i][j] is not None:
                                        fltk.efface(grille_global[i][j] + f"_{i-dy}_{j-dx}")
                                    grille_global[i][j] = "SSSS"
                                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille_global[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille_global[i][j] + f"_{i}_{j}")
                elif touche == "r":
                    riviere = not riviere
                    print(f"Contraitne riviere : {riviere}")
                elif touche == "f": #Zoom in / il faut verifier si autour de la ou on veux afficher y a des tuiles
                    generation_forced = False
                    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
                    i, j = convert_click_indice(x, y)
                    #efface_grille_displayed(grille_affiche)
                    efface_2()
                    NB_CASES = NB_CASES - 2 if NB_CASES > 2 else NB_CASES
                    dx, dy = dx + j - NB_CASES//2, dy + i - NB_CASES//2
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                elif touche == "g": #Zoom out
                    generation_forced = False
                    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
                    i, j = convert_click_indice(x, y)
                    #efface_grille_displayed(grille_affiche)
                    efface_2()
                    NB_CASES = NB_CASES + 2 if NB_CASES <= 20 and NB_CASES <= len(grille_global) - 2 else NB_CASES
                    dx, dy = dx + j - NB_CASES//2, dy + i - NB_CASES//2
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                
                #MOVEMENT
                if touche == "z":  # haut
                    if generation_forced:
                        generation = True
                    efface_2()
                    grille_global = [[None] * len(grille_global[0])] + grille_global if dy == 0 else grille_global
                    dy = dy-1 if dy > 0 else 0
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                elif touche == "s":  # bas
                    if generation_forced:
                        generation = True
                    efface_2()
                    grille_global = grille_global + [[None] * len(grille_global[0])] if dy == len(grille_global) - NB_CASES else grille_global
                    dy += 1
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                elif touche == "q":  # gauche
                    if generation_forced:
                        generation = True
                    efface_2()
                    if dx == 0:
                        for i in range(len(grille_global)):
                            grille_global[i] = [None] + grille_global[i]
                    dx = dx-1 if dx > 0 else 0
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                elif touche == "d":  # droite
                    if generation_forced:
                        generation = True
                    efface_2()
                    if dx >= len(grille_global[0]) - NB_CASES:
                        for i in range(len(grille_global)):
                            grille_global[i] = grille_global[i] + [None]
                    dx += 1
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
            else:
                if touche == "Down":
                    if len(tuiles_possibles) > 25:
                        decale = decale + 1 if decale < len(tuiles_possibles) - 25 else decale
                        fltk.efface("choices_display")
                        fltk.efface("scroll_bar")
                        for tuile in tuiles_possibles_affiche:
                                fltk.efface(tuile["nom"])
                        tuiles_possibles_affiche = tuiles_possibles[decale:25+decale]
                        champs_possibilites(tuiles_possibles_affiche)
                        scroll_bar(len(tuiles_possibles), decale)
                elif touche == "Up":
                    if len(tuiles_possibles) > 25:
                        decale = decale - 1 if decale > 0 else 0
                        fltk.efface("choices_display")
                        fltk.efface("scroll_bar")
                        for tuile in tuiles_possibles_affiche:
                                fltk.efface(tuile["nom"])
                        tuiles_possibles_affiche = tuiles_possibles[decale:25+decale]
                        champs_possibilites(tuiles_possibles_affiche)
                        scroll_bar(len(tuiles_possibles), decale)
                
    #generation infini
    if generation and generation_forced:
        generation = False
        if generator(grille_affiche, tuiles, riviere):
            for i in range(len(grille_affiche)):
                for j in range(len(grille_affiche[0])):
                    if grille_global[i + dy][j + dx] is None:
                        grille_global[i + dy][j + dx] = grille_affiche[i][j]
                    k, l = convert_indice_click(i, j)
                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille_affiche[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille_affiche[i][j] + f"_{i}_{j}")
        else:
            print("Pas de solution")
    fltk.mise_a_jour()
    