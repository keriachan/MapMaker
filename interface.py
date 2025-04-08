from modules import fltk, gestion_tuiles, reader, solver
import random

WIDTH, HEIGHT = 500, 500
MARGIN = 100
NB_CASES = 10

def convert_click_indice(x, y):#pour 10x10
    return int(y//(HEIGHT/NB_CASES)), int(x//(WIDTH/NB_CASES))

def convert_indice_click(i, j):#pour 10x10
    return int(j*(HEIGHT/NB_CASES)), int(i*(WIDTH/NB_CASES))

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

def decale_grille(grille: list[list[str]], dx: int, dy: int):
    nouvelle_grille = [[None for _ in range(NB_CASES)] for _ in range(NB_CASES)]

    for i in range(NB_CASES):
        for j in range(NB_CASES):
            new_i, new_j = i - dy, j - dx
            if 0 <= new_i < NB_CASES and 0 <= new_j < NB_CASES:
                nouvelle_grille[i][j] = grille[new_i][new_j]

    # Efface ancienne grille
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            if grille[i][j] is not None:
                fltk.efface(grille[i][j] + f"_{i}_{j}")

    # Affiche nouvelle grille
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            if nouvelle_grille[i][j] is not None:
                k, l = convert_indice_click(i, j)
                fltk.image(k, l, "fichiers fournis/tuiles/" + nouvelle_grille[i][j] + ".png",
                           WIDTH // NB_CASES, HEIGHT // NB_CASES, "nw", nouvelle_grille[i][j] + f"_{i}_{j}")
    for i in range(NB_CASES):
        grille[i] = nouvelle_grille[i]
        
fltk.cree_fenetre(WIDTH, HEIGHT)
fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")

grille = [[None] * NB_CASES for _ in range(NB_CASES)]
tuiles = reader.cree_dico("fichiers fournis/tuiles/")
choix = False
generation = False

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        if fltk.type_ev(ev) == "Quitte":
            break
        elif fltk.type_ev(ev) == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille[i][j] is not None:
                    continue
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille, i, j)
                if len(tuiles_possibles) == 0:
                    print("Pas de tuiles possibles")
                    continue
                tuiles_possibles_alea = tuiles_possibles if len(tuiles_possibles) <= 25 else random.sample(tuiles_possibles, 25)
                champs_possibilites(tuiles_possibles_alea)
                choix = True
            else:
                i, j = convert_click_indice(k, l)
                if tuiles_possibles_alea is not None:
                    for tuile in tuiles_possibles_alea:
                        if fltk.est_objet_survole(tuile["nom"]):
                            choix = False
                            fltk.efface("choices_display")
                            for tuile_bis in tuiles_possibles_alea:
                                fltk.efface(tuile_bis["nom"])
                            grille[i][j] = tuile["nom"]
                            fltk.image(k, l, tuile["chemin"], WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", tuile["nom"] + f"_{i}_{j}")
                            break
        elif fltk.type_ev(ev) == "ClicDroit":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille[i][j] is not None:
                        fltk.efface(grille[i][j] + f"_{i}_{j}")
                        grille[i][j] = None
        elif fltk.type_ev(ev) == "Touche":
            touche = fltk.touche(ev)
            if touche == "p":#profondeur
                generation = True
            elif touche == "l":#largeur trop lent
                if solver.solver_largeur(grille, tuiles):
                    print("ui")
                    for i in range(len(grille)):
                        for j in range(len(grille[0])):
                            k, l = convert_indice_click(i, j)
                            fltk.image(k, l, "fichiers fournis/tuiles/" + grille[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille[i][j] + f"_{i}_{j}")
            #MOVEMENT
            if touche == "z":  # haut
                generation = True
                decale_grille(grille, dx=0, dy=1)
            elif touche == "s":  # bas
                generation = True
                decale_grille(grille, dx=0, dy=-1)
            elif touche == "q":  # gauche
                generation = True
                decale_grille(grille, dx=1, dy=0)
            elif touche == "d":  # droite
                generation = True
                decale_grille(grille, dx=-1, dy=0)
    if generation:
        generation = False
        if solver.solver_profondeur(grille, tuiles):
            for i in range(len(grille)):
                for j in range(len(grille[0])):
                    k, l = convert_indice_click(i, j)
                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille[i][j] + f"_{i}_{j}")
    fltk.mise_a_jour()
    