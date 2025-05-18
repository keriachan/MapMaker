from modules import fltk, gestion_tuiles, reader, solver
import random, copy, string


WIDTH, HEIGHT = 1000, 1000
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
    """
    Dessine une barre de défilement verticale en fonction de la taille totale des éléments 
    et de la position actuelle du décalage (élément affiché en haut).

    Paramètres :
    - taille (int) : nombre total d'éléments affichables (par exemple, lignes dans une liste).
    - decale (int) : indice de l'élément actuellement en haut de l'affichage (décalage).
    """
    max_height = HEIGHT - 2 * MARGIN
    bar_height = max_height * min(1, 25 / taille)
    y1 = MARGIN + (decale / max(1, taille - 25)) * (max_height - bar_height)
    y2 = y1 + bar_height
    fltk.rectangle(WIDTH - MARGIN - 12, y1, WIDTH - MARGIN - 2, y2, "black", "grey", 1, "scroll_bar")

def position_to_decale(y, taille):
    """
    Convertit une position verticale (y) sur la barre de défilement en décalage logique 
    correspondant à l'indice de l'élément à afficher en haut.

    Paramètres :
    - y (float) : position verticale du curseur (souvent cliquée ou déplacée).
    - taille (int) : nombre total d’éléments affichables.

    Retour :
    - decale (int) : indice de l’élément correspondant à la position y.
    """
    max_height = HEIGHT - 2 * MARGIN
    bar_height = max_height * min(1, 25 / taille)
    
    y_rel = (y - MARGIN - bar_height / 2) / (max_height - bar_height)
    y_rel = min(max(0, y_rel), 1)  

    decale = round(y_rel * max(0, taille - 25))
    return decale

def affiche_menu():
    fltk.rectangle(MARGIN, MARGIN//10, WIDTH - MARGIN, MARGIN//10 + HEIGHT//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH//2, MARGIN//10 + HEIGHT//16, "MENU", "black", "white", "center",taille=WIDTH//16, tag="menu")
    
    #new map
    fltk.rectangle(MARGIN//10, MARGIN*2//10 + HEIGHT//8, WIDTH//2 - MARGIN//20, MARGIN*2//10 + HEIGHT*2//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH//4, MARGIN*2//10 + HEIGHT//8 + HEIGHT//16, "Nouvelle carte", "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag="menu")
    
    #nom de la carte
    fltk.rectangle(MARGIN//10, MARGIN*3//10 + HEIGHT*2//8, WIDTH//2 - MARGIN//20, MARGIN*3//10 + HEIGHT*2//8 + HEIGHT//16, "black", "white", 1, "menu")
    fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (MARGIN*3//10 + HEIGHT*2//8 + MARGIN*3//10 + HEIGHT*2//8 + HEIGHT//16)//2, "Nom de la carte :", "black", "white", "center", taille=WIDTH//40, tag="menu")
    
    fltk.rectangle(MARGIN//10, MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16, WIDTH//2 - MARGIN//20, MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16, "black", "white", 1, "nom_carte")
    fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2, "Nom_de_la_carte", "black", "white", "center", taille=WIDTH//40, tag="nom_carte_texte")
    
    #largeur
    fltk.rectangle(MARGIN//10, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//20 - WIDTH//8, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, "Largeur de la carte :", "black", "white", "center", taille=WIDTH//40, tag="menu")
    
    fltk.rectangle(WIDTH//2 + MARGIN//20 - WIDTH//8, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//10 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=WIDTH//40, tag="largeur_case")
    
    fltk.rectangle(WIDTH//2 - MARGIN/20 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16, WIDTH//2 - MARGIN//20, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 - MARGIN//40, "black", "white", 1, "up_largeur")
    fltk.texte((WIDTH//2 - MARGIN/20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 - MARGIN//40)//2, "up", "black", "white", "center", taille=WIDTH//80, tag="menu")
    
    fltk.rectangle(WIDTH//2 - MARGIN/20 - WIDTH//32, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 + MARGIN//40, WIDTH//2 - MARGIN//20, MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT*2//32, "black", "white", 1, "down_largeur")
    fltk.texte((WIDTH//2 - MARGIN/20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT//32 + MARGIN//40 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + HEIGHT*2//32)//2, "down", "black", "white", "center", taille=WIDTH//114, tag="menu") #police 7 pour taille 800
    
    #hauteur
    fltk.rectangle(MARGIN//10,  MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16,  WIDTH//2 - MARGIN//20 - WIDTH//8,  MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, "Hauteur de la carte :", "black", "white", "center", taille=WIDTH//40, tag="menu")
    
    fltk.rectangle(WIDTH//2 + MARGIN//20 - WIDTH//8, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16, WIDTH//2 - MARGIN//10 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16, "black", "white", 1, "menu")
    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=WIDTH//40, tag="hauteur_case")

    fltk.rectangle(WIDTH//2 - MARGIN//20 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16, WIDTH//2 - MARGIN//20, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 - MARGIN//40, "black", "white", 1, "up_hauteur")
    fltk.texte((WIDTH//2 - MARGIN//20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 - MARGIN//40)//2, "up", "black", "white", "center", taille=WIDTH//80, tag="menu")

    fltk.rectangle(WIDTH//2 - MARGIN//20 - WIDTH//32, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 + MARGIN//40, WIDTH//2 - MARGIN//20, MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT*2//32, "black", "white", 1, "down_hauteur")
    fltk.texte((WIDTH//2 - MARGIN//20 - WIDTH//32 + WIDTH//2 - MARGIN//20)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT//32 + MARGIN//40 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + HEIGHT*2//32)//2, "down", "black", "white", "center", taille=WIDTH//114, tag="menu")

    #LANCER
    fltk.rectangle(MARGIN//10, HEIGHT - HEIGHT//8 - MARGIN//10, WIDTH//2 - MARGIN//20, HEIGHT - MARGIN//10, "black", "white", 1, "new_map")
    fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (HEIGHT - HEIGHT//8 - MARGIN//10 + HEIGHT - MARGIN//10)//2, "Commencer", "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag="new_map")
    
    #load map
    fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*2//10 + HEIGHT//8, WIDTH - MARGIN//10, MARGIN*2//10 + HEIGHT*2//8, "black", "white", 1, "menu")
    fltk.texte(WIDTH*3//4, MARGIN*2//10 + HEIGHT//8 + HEIGHT//16, "Charger une carte", "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag="menu")
    
    #map sauvegardée
    fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*3//10 + HEIGHT*2//8, WIDTH - MARGIN//10, HEIGHT - HEIGHT//8 - MARGIN*2//10, "black", "white", 1, tag="load_map_saved")
    data = reader.read()
    longueur = len(data) if len(data) < 5 else 5
    taille = (HEIGHT - HEIGHT//8 - MARGIN*2//10 - (MARGIN*3//10 + HEIGHT*2//8))//5
    for i in range(longueur):
        name = data[i]["nom_carte"]
        fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*3//10 + HEIGHT*2//8 + (i * taille), WIDTH - MARGIN//10, MARGIN*3//10 + HEIGHT*2//8 + ((i + 1) * taille), "black",remplissage="white", epaisseur=1, tag=f"rect_{name}")
        fltk.texte(WIDTH*3//4, MARGIN*3//10 + HEIGHT*2//8  + taille//2 + (i * taille), name, "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag=f"{name}")

    #LANCER
    fltk.rectangle(WIDTH//2 + MARGIN//20, HEIGHT - HEIGHT//8 - MARGIN//10, WIDTH - MARGIN//10, HEIGHT - MARGIN//10, "black", "white", 1, tag="rect_load_map")
    fltk.texte((WIDTH//2 + MARGIN//20 + WIDTH - MARGIN//10)//2, (HEIGHT - HEIGHT//8 - MARGIN//10 + HEIGHT - MARGIN//10)//2, "Charger", "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag="load_map")
    
fltk.cree_fenetre(WIDTH, HEIGHT)
fltk.rectangle(0, 0, WIDTH, HEIGHT, remplissage="lightgrey", tag="background")
affiche_menu()
menu = True
champ_texte = False
nom_carte = "Nom_de_la_carte"
caracteres_valides = string.ascii_letters + string.digits + string.punctuation
text_cursor = len(nom_carte)
cursor = None
curseur_visible = True
temps_derniere_alternance = fltk.time()
data = reader.read()

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        if not menu:
            grille_affiche = decale_grille_displayed(grille_global, dy, dx)
        if fltk.type_ev(ev) == "Quitte":
            if not menu:
                reader.save_json(grille_global, nom_carte)
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
                    decale = 0
                    scroll_bar(len(tuiles_possibles), decale)
                    choix = True
                else:
                    if  WIDTH - MARGIN - 12 <= x <= WIDTH - MARGIN - 2 and MARGIN <= y <= HEIGHT - MARGIN:
                        if len(tuiles_possibles) > 25:
                            decale = position_to_decale(y, len(tuiles_possibles))
                            fltk.efface("choices_display")
                            fltk.efface("scroll_bar")
                            for tuile in tuiles_possibles_affiche:
                                fltk.efface(tuile["nom"])
                            tuiles_possibles_affiche = tuiles_possibles[decale:25+decale]
                            champs_possibilites(tuiles_possibles_affiche)
                            scroll_bar(len(tuiles_possibles), decale)
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
                champ_texte = False
                if fltk.est_objet_survole("up_largeur"):
                    NB_CASES[0] = NB_CASES[0] + 1 if NB_CASES[0] < 50 else NB_CASES[0]
                    fltk.efface("largeur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=WIDTH//40, tag="largeur_case")
                elif fltk.est_objet_survole("down_largeur"):
                    NB_CASES[0] = NB_CASES[0] - 1 if NB_CASES[0] > 2 else NB_CASES[0]
                    fltk.efface("largeur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*4//10 + HEIGHT*3//8 + HEIGHT//16 + MARGIN*4//10 + HEIGHT*3//8 + HEIGHT*2//16)//2, f"{NB_CASES[0]}", "black", "white", "center", taille=WIDTH//40, tag="largeur_case")
                elif fltk.est_objet_survole("up_hauteur"):
                    NB_CASES[1] = NB_CASES[1] + 1 if NB_CASES[1] < 50 else NB_CASES[1]
                    fltk.efface("hauteur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=WIDTH//40, tag="hauteur_case")
                elif fltk.est_objet_survole("down_hauteur"):
                    NB_CASES[1] = NB_CASES[1] - 1 if NB_CASES[1] > 2 else NB_CASES[1]
                    fltk.efface("hauteur_case")
                    fltk.texte((WIDTH//2 + MARGIN//20 - WIDTH//8 + WIDTH//2 - MARGIN//10 - WIDTH//32)//2, (MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*2//16 + MARGIN*5//10 + HEIGHT*3//8 + HEIGHT*3//16)//2, f"{NB_CASES[1]}", "black", "white", "center", taille=WIDTH//40, tag="hauteur_case")
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
                elif fltk.est_objet_survole("nom_carte"):
                    champ_texte = True
                elif fltk.est_objet_survole("load_map_saved"):
                    longueur = len(data) if len(data) < 5 else 5
                    taille = (HEIGHT - HEIGHT//8 - MARGIN*2//10 - (MARGIN*3//10 + HEIGHT*2//8))//5
                    for i in range(longueur):
                        name = data[i]["nom_carte"]
                        obj = f"rect_{name}"
                        if fltk.est_objet_survole(obj):
                            map_data = data[i]
                            couleur = "grey"
                        else:
                            couleur = "white"
                        fltk.efface(obj)
                        fltk.efface(name)
                        fltk.rectangle(WIDTH//2 + MARGIN//20, MARGIN*3//10 + HEIGHT*2//8 + (i * taille), WIDTH - MARGIN//10, MARGIN*3//10 + HEIGHT*2//8 + ((i + 1) * taille), "black",remplissage=couleur, epaisseur=1, tag=f"rect_{name}")
                        fltk.texte(WIDTH*3//4, MARGIN*3//10 + HEIGHT*2//8  + taille//2 + (i * taille), name, "black", "white", "center", taille=WIDTH//16 - WIDTH//40, tag=f"{name}")
                elif fltk.est_objet_survole("rect_load_map"):
                    efface_2()
                    menu = False
                    grille_global = map_data["grille"]
                    nom_carte = map_data["nom_carte"]
                    dx , dy = 0, 0 #coin supérieur gauche de la grille affichée par rapport à la grille globale
                    tuiles = reader.cree_dico("fichiers fournis/tuiles/")
                    choix = False
                    generation = True
                    generation_forced = False
                    riviere = False
                    decale = 0 #decale pour le scroll
                    display_grille(grille_global)
                if not champ_texte:
                    fltk.efface(cursor)
        elif fltk.type_ev(ev) == "ClicDroit":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if not menu and not choix:
                i, j = convert_click_indice(x, y)
                k, l = convert_indice_click(i, j)
                if grille_global[i+dy][j+dx] is not None:
                        fltk.efface(grille_affiche[i][j] + f"_{i}_{j}")
                        grille_global[i+dy][j+dx] = None
        elif fltk.type_ev(ev) == "Touche":
            touche = fltk.touche(ev)
            if not menu:
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
            else:
                if champ_texte:
                    width_txt, _ = fltk.taille_texte(nom_carte, taille=WIDTH//40)
                    if width_txt < WIDTH//2 - MARGIN//20 - MARGIN*2//10:
                        if touche in caracteres_valides:
                            nom_carte = nom_carte[:text_cursor] + touche + nom_carte[text_cursor:]
                            text_cursor += 1
                            fltk.efface("nom_carte_texte")
                            fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2, nom_carte, "black", "white", "center", taille=WIDTH//40, tag="nom_carte_texte")
                        #elif touche == "space":
                        #    nom_carte = nom_carte[:text_cursor] + " " + nom_carte[text_cursor:]
                        #    text_cursor += 1
                        #    fltk.efface("nom_carte_texte")
                        #    fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2, nom_carte, "black", "white", "center", taille=WIDTH//40, tag="nom_carte_texte")
                    if touche == "BackSpace":
                        nom_carte = nom_carte[:text_cursor-1] + nom_carte[text_cursor:]
                        text_cursor -= 1 if text_cursor > 0 else 0
                        fltk.efface("nom_carte_texte")
                        fltk.texte((MARGIN//10 + WIDTH//2 - MARGIN//20)//2, (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2, nom_carte, "black", "white", "center", taille=WIDTH//40, tag="nom_carte_texte")
                    elif touche == "Return":
                        champ_texte = False
                        fltk.efface(cursor)
                    elif touche == "Left":
                        text_cursor = text_cursor - 1 if text_cursor > 0 else 0
                    elif touche == "Right":
                        text_cursor = text_cursor + 1 if text_cursor < len(nom_carte) else text_cursor
    if menu and champ_texte:
        if cursor:
            fltk.efface(cursor)
        width_txt, height_txt = fltk.taille_texte(nom_carte, taille=WIDTH//40)
        width_left, _ = fltk.taille_texte(nom_carte[:text_cursor], taille=WIDTH//40)
        current = fltk.time()
        if current - temps_derniere_alternance > 0.5:
            curseur_visible = not curseur_visible
            temps_derniere_alternance = current
        if curseur_visible:
            x_cursor = (MARGIN//10 + WIDTH//2 - MARGIN//20)//2 - width_txt  // 2 + width_left
            y_top = (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2 - height_txt // 2
            y_bot = (MARGIN*4//10 + HEIGHT*2//8 + HEIGHT//16 + MARGIN*3//10 + HEIGHT*3//8 + HEIGHT//16)//2 + height_txt // 2
            cursor = fltk.ligne(x_cursor, y_top, x_cursor, y_bot, couleur="black", epaisseur=2)
            
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
    