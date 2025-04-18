from modules import fltk, gestion_tuiles, reader, solver
import random, copy


WIDTH, HEIGHT = 800, 800
MARGIN = WIDTH//5
NB_CASES = [10, 10] #largeur, hauteur de la grille

def convert_click_indice(x, y):#pour 10x10
    return int(y//(HEIGHT/NB_CASES[1])), int(x//(WIDTH/NB_CASES[0]))

def convert_indice_click(i, j):#pour 10x10
    return int(j*(WIDTH/NB_CASES[0])), int(i*(HEIGHT/NB_CASES[1]))

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
    for i in range(NB_CASES[1]):
        for j in range(NB_CASES[0]):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None:
                fltk.efface(grille[i][j] + f"_{i}_{j}")
                
def display_grille(grille: list[list[str]]):
    for i in range(NB_CASES[1]):
        for j in range(NB_CASES[0]):
            if 0 <= i < len(grille) and 0 <= j < len(grille[0]) and grille[i][j] is not None: # peut etre faire un exept pour eviter une erreur out of ranges
                k, l = convert_indice_click(i, j)
                fltk.image(k, l, "fichiers fournis/tuiles/" + grille[i][j] + ".png", WIDTH//NB_CASES[0], HEIGHT//NB_CASES[1], "nw", grille[i][j] + f"_{i}_{j}")
   
def decale_grille_displayed(grille, dy, dx):
    """ dy, dx est le coin supérieur gauche de la grille a afficher """
    grille_temp = []
    for i in range(dy, NB_CASES[1] + dy):
        ligne_temp = []
        for j in range(dx, NB_CASES[0] + dx):
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

def affiche_menu():
    fltk.rectangle(MARGIN, MARGIN//10, WIDTH - MARGIN, MARGIN//10 + HEIGHT//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH//2, MARGIN//10 + HEIGHT//16, "MENU", "black", "white", "center",taille=50, tag="menu")
    
    #fltk.rectangle(MARGIN//10, MARGIN*2//10 + HEIGHT//8, WIDTH//2 - MARGIN//20, HEIGHT - MARGIN//10, "black", "white", 1, "menu")#fond new map
    #fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*2//10 + HEIGHT//8, WIDTH - MARGIN//10, HEIGHT - MARGIN//10, "black", "white", 1, "menu")#fond load map
    
    #new map
    fltk.rectangle(MARGIN//10, MARGIN*2//10 + HEIGHT//8, WIDTH//2 - MARGIN//20, MARGIN*2//10 + HEIGHT*2//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH//4, MARGIN*2//10 + HEIGHT//8 + HEIGHT//16, "Nouvelle carte", "black", "white", "center", taille=30, tag="menu")
    
    fltk.rectangle(MARGIN//10, MARGIN*3//10 + HEIGHT*2//8, WIDTH//2 - MARGIN//20, MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16, "black", "white", 1, "menu")
    fltk.texte(MARGIN*2//10, MARGIN*2//10 + HEIGHT//8 + HEIGHT//16 + HEIGHT//8, "Nom de la carte :", "black", "white", "nw", taille=20, tag="menu")
    
    #largeur
    fltk.rectangle(MARGIN//10, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//20 - WIDTH//8, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, "Largeur de la carte :", "black", "white", "center", taille=20, tag="menu")
    
    fltk.rectangle(WIDTH//2 + MARGIN//20 - WIDTH//8, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//10 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=20, tag="largeur_case")
    
    fltk.rectangle(WIDTH//2 - MARGIN/20 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//20, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 - MARGIN//40, "black", "white", 1, "up_largeur")
    fltk.texte((WIDTH//2 - MARGIN/20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 - MARGIN//40)//2, "up", "black", "white", "center", taille=10, tag="menu")
    
    fltk.rectangle(WIDTH//2 - MARGIN/20 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 + MARGIN//40, WIDTH//2 - MARGIN//20, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT*2//32, "black", "white", 1, "down_largeur")
    fltk.texte((WIDTH//2 - MARGIN/20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 + MARGIN//40 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT*2//32)//2, "down", "black", "white", "center", taille=7, tag="menu")
    
    #hauteur
    fltk.rectangle(MARGIN//10,  MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16,  WIDTH//2 - MARGIN//20 - WIDTH//8,  MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, "Hauteur de la carte :", "black", "white", "center", taille=20, tag="menu")
    
    fltk.rectangle(WIDTH//2 + MARGIN//20 - WIDTH//8, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16, WIDTH//2 - MARGIN//10 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=20, tag="hauteur_case")

    fltk.rectangle(WIDTH//2 - MARGIN//20 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16, WIDTH//2 - MARGIN//20, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 - MARGIN//40, "black", "white", 1, "up_hauteur")
    fltk.texte((WIDTH//2 - MARGIN//20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 - MARGIN//40)//2, "up", "black", "white", "center", taille=10, tag="menu")

    fltk.rectangle(WIDTH//2 - MARGIN//20 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 + MARGIN//40, WIDTH//2 - MARGIN//20, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT*2//32, "black", "white", 1, "down_hauteur")
    fltk.texte((WIDTH//2 - MARGIN//20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 + MARGIN//40 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT*2//32)//2, "down", "black", "white", "center", taille=7, tag="menu")

    #LANCER
    fltk.rectangle(MARGIN//10, HEIGHT - HEIGHT//8 - MARGIN//10, WIDTH//2 - MARGIN//20, HEIGHT - MARGIN//10, "black", "white", 1, "new_map")
    fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (HEIGHT - HEIGHT//8 - MARGIN//10 + HEIGHT - MARGIN//10)//2, "Commencer", "black", "white", "center", taille=30, tag="new_map")
    
    #load map
    fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*2//10 + HEIGHT//8, WIDTH - MARGIN//10, MARGIN*2//10 + HEIGHT*2//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH*3//4, MARGIN*2//10 + HEIGHT//8 + HEIGHT//16, "Charger une carte", "black", "white", "center", taille=30, tag="menu")
    
    #map sauvegardée
    fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*3//10 + HEIGHT*2//8, WIDTH - MARGIN//10, HEIGHT - HEIGHT//8 - MARGIN*2//10, "black", "white", 1, "menu")
    
    #LANCER
    fltk.rectangle(WIDTH//2 + MARGIN//20, HEIGHT - HEIGHT//8 - MARGIN//10, WIDTH - MARGIN//10, HEIGHT - MARGIN//10, "black", "white", 1, "load_map")
    fltk.texte((WIDTH//2 + MARGIN//20 + WIDTH - MARGIN//10)//2, (HEIGHT - HEIGHT//8 - MARGIN//10 + HEIGHT - MARGIN//10)//2, "Charger", "black", "white", "center", taille=30, tag="load_map")
    
fltk.cree_fenetre(WIDTH, HEIGHT)
fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")
affiche_menu()
menu = True

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        if not menu:
            grille_affiche = decale_grille_displayed(grille_global, dy, dx)
        if fltk.type_ev(ev) == "Quitte":
            break
        elif fltk.type_ev(ev) == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not menu:
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
                                fltk.image(k, l, tuile["chemin"], WIDTH//NB_CASES[0], HEIGHT//NB_CASES[1], "nw", tuile["nom"] + f"_{i}_{j}")
                                break
            else:
                if fltk.est_objet_survole("up_largeur"):
                    NB_CASES[0] = NB_CASES[0] + 1 if NB_CASES[0] < 50 else NB_CASES[0]
                    fltk.efface("largeur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=20, tag="largeur_case")
                elif fltk.est_objet_survole("down_largeur"):
                    NB_CASES[0] = NB_CASES[0] - 1 if NB_CASES[0] > 2 else NB_CASES[0]
                    fltk.efface("largeur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=20, tag="largeur_case")
                elif fltk.est_objet_survole("up_hauteur"):
                    NB_CASES[1] = NB_CASES[1] + 1 if NB_CASES[1] < 50 else NB_CASES[1]
                    fltk.efface("hauteur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=20, tag="hauteur_case")
                elif fltk.est_objet_survole("down_hauteur"):
                    NB_CASES[1] = NB_CASES[1] - 1 if NB_CASES[1] > 2 else NB_CASES[1]
                    fltk.efface("hauteur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=20, tag="hauteur_case")
                elif fltk.est_objet_survole("new_map"):
                    efface_2()
                    menu = False
                    grille_global = [[None] * NB_CASES[0] for _ in range(NB_CASES[1])]
                    dx , dy = 0, 0 #coin supérieur gauche de la grille affichée par rapport à la grille globale
                    tuiles = reader.cree_dico("fichiers fournis/tuiles/")
                    choix = False
                    generation = True
                    generation_forced = False
                    riviere = False
                    decale = 0 #decale pour le scroll
                     
                    
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
                    grille_global = [[None] * NB_CASES[0] for _ in range(NB_CASES[1])]
                    dx, dy = 0, 0
                elif touche == "a": #arrete la generation
                    generation_forced = False
                elif touche == "m": #mer sur le bord de la grille
                    for i in range(dy, NB_CASES[1] + dy):
                        for j in range(dx, NB_CASES[0] + dx):
                            if i == dy or i == dy + NB_CASES[1] - 1 or j == dx or j == dx + NB_CASES[0] - 1:
                                k, l = convert_indice_click(i, j)
                                if grille_global[i][j] != "SSSS" and gestion_tuiles.emplacement_valide(grille_global, i, j, "SSSS"):
                                    if grille_global[i][j] is not None:
                                        fltk.efface(grille_global[i][j] + f"_{i-dy}_{j-dx}")
                                    grille_global[i][j] = "SSSS"
                                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille_global[i][j] + ".png", WIDTH//NB_CASES[0], HEIGHT//NB_CASES[1], "nw", grille_global[i][j] + f"_{i}_{j}")
                elif touche == "r":
                    riviere = not riviere
                    print(f"Contraitne riviere : {riviere}")
                elif touche == "f": #Zoom in / il faut verifier si autour de la ou on veux afficher y a des tuiles
                    generation_forced = False
                    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
                    i, j = convert_click_indice(x, y)
                    efface_2()
                    NB_CASES = [e - 2 if e > 2 else e for e in NB_CASES] if sum(e > 2 for e in NB_CASES) != 1 else NB_CASES# peut etre faux
                    dx, dy = dx + j - NB_CASES[0]//2, dy + i - NB_CASES[1]//2
                    grille_affiche = decale_grille_displayed(grille_global, dy, dx)
                    display_grille(grille_affiche)
                elif touche == "g": #Zoom out
                    generation_forced = False
                    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
                    i, j = convert_click_indice(x, y)
                    #efface_grille_displayed(grille_affiche)
                    efface_2()
                    NB_CASES = [e + 2 if e <= 50 and e <= len(grille_global) - 2 else e for e in NB_CASES] if sum(e <= 50 and e <= len(grille_global) - 2 for e in NB_CASES) != 1 else NB_CASES # peut etre faux
                    dx, dy = dx + j - NB_CASES[0]//2, dy + i - NB_CASES[1]//2
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
                    grille_global = grille_global + [[None] * len(grille_global[0])] if dy == len(grille_global) - NB_CASES[1] else grille_global
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
                    if dx >= len(grille_global[0]) - NB_CASES[0]:
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
    if not menu and generation and generation_forced:
        generation = False
        grille_temp = copy.deepcopy(grille_affiche)
        if generator(grille_affiche, tuiles, riviere):
            for i in range(len(grille_affiche)):
                for j in range(len(grille_affiche[0])):
                    if grille_global[i + dy][j + dx] is None:
                        grille_global[i + dy][j + dx] = grille_affiche[i][j]
                    k, l = convert_indice_click(i, j)
                    fltk.image(k, l, "fichiers fournis/tuiles/" + grille_affiche[i][j] + ".png", WIDTH//NB_CASES[0], HEIGHT//NB_CASES[1], "nw", grille_affiche[i][j] + f"_{i}_{j}")
        else:
            grille_affiche = copy.deepcopy(grille_temp)
            print("Pas de solution")
    fltk.mise_a_jour()
    