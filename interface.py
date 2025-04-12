from modules import fltk, gestion_tuiles, reader, solver
import random

WIDTH, HEIGHT = 800, 800
MARGIN = WIDTH//5
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

def efface_grille_displayed(grille):
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None:
                fltk.efface(grille[i][j] + f"_{i}_{j}")
                
def decale_grille(grille: list[list[str]], dy: int, dx: int):
    for i in range(dy, NB_CASES + dy):
        for j in range(dx, NB_CASES + dx):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None: # peut etre faire un exept pour eviter une erreur out of ranges
                k, l = convert_indice_click(i - dy, j - dx)
                fltk.image(k, l, "fichiers fournis/tuiles/" + grille[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille[i][j] + f"_{i - dy}_{j - dx}")
       
def display_grille(grille, i, j):
    """ i, j est le coin supérieur gauche de la grille a afficher """
    grille_temp = []
    for k in range(i, NB_CASES + i):
        ligne_temp = []
        for l in range(j, NB_CASES + j):
            if 0 <= k < len(grille) and 0 <= l < len(grille[0]):
                ligne_temp.append(grille[k][l])
        grille_temp.append(ligne_temp)
    return grille_temp
 
fltk.cree_fenetre(WIDTH, HEIGHT)
fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")

grille_global = [[None] * NB_CASES for _ in range(NB_CASES)]
dx , dy = 0, 0 #coin supérieur gauche de la grille affichée par rapport à la grille globale
tuiles = reader.cree_dico("fichiers fournis/tuiles/")
choix = False
generation = True
generation_forced = False

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        grille_affiche = display_grille(grille_global, dy, dx)
        if fltk.type_ev(ev) == "Quitte":
            break
        elif fltk.type_ev(ev) == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille_affiche[i][j] is not None:
                    continue
                tuiles_possibles = gestion_tuiles.tuiles_possibles(tuiles, grille_affiche, i, j)
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
            if touche == "p":#profondeur
                generation_forced = True
                generator = solver.solver_profondeur
            elif touche == "l":#largeur trop lent
                generation_forced = True
                generator = solver.solver_largeur
            elif touche == "c":#contrainte
                generation_forced = True
                generator = solver.solver_profondeur_contrainte
            elif touche == "e":#efface
                efface_grille_displayed(grille_affiche)
                grille_global = [[None] * NB_CASES for _ in range(NB_CASES)]
                dx, dy = 0, 0
            elif touche == "a": #arrete la generation
                generation_forced = False
                
            #MOVEMENT
            if touche == "z":  # haut
                if generation_forced:
                    generation = True
                efface_grille_displayed(grille_affiche)
                grille_global = [[None] * NB_CASES] + grille_global if dy == 0 else grille_global
                dy = dy-1 if dy > 0 else 0
                decale_grille(grille_global, dy, dx)
            elif touche == "s":  # bas
                if generation_forced:
                    generation = True
                efface_grille_displayed(grille_affiche)
                grille_global = grille_global + [[None] * NB_CASES] if dy == len(grille_global) - NB_CASES else grille_global
                dy += 1
                decale_grille(grille_global, dy, dx)
            elif touche == "q":  # gauche
                if generation_forced:
                    generation = True
                efface_grille_displayed(grille_affiche)
                if dx == 0:
                    grille_temp = []
                    for i in range(len(grille_global)):
                        grille_temp.append([None] + grille_global[i])
                    grille_global = grille_temp
                dx = dx-1 if dx > 0 else 0
                decale_grille(grille_global, dy, dx)
            elif touche == "d":  # droite
                if generation_forced:
                    generation = True
                efface_grille_displayed(grille_affiche)
                if dx == len(grille_global[0]) - NB_CASES:
                    grille_temp = []
                    for i in range(len(grille_global)):
                        grille_temp.append(grille_global[i] + [None])
                    grille_global = grille_temp
                dx += 1
                decale_grille(grille_global, dy, dx)
    
    #generation infini
    if generation and generation_forced:
        generation = False
        print(f"{generator.__name__} en cours...")
        grille_affiche = display_grille(grille_global, dy, dx)
        if generator(grille_affiche, tuiles):
            for i in range(len(grille_affiche)):
                for j in range(len(grille_affiche[0])):
                    if grille_global[i + dy][j + dx] is None:
                        grille_global[i + dy][j + dx] = grille_affiche[i][j]
                    k, l = convert_indice_click(i, j)
                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille_affiche[i][j] + ".png", WIDTH//NB_CASES, HEIGHT//NB_CASES, "nw", grille_affiche[i][j] + f"_{i}_{j}")
    fltk.mise_a_jour()
    