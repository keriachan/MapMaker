from modules import fltk
from modules import reader
from modules import gestion_truiles
import random

WIDTH, HEIGHT = 500, 500
MARGIN = 100
NB_CASES = 10
def detect_case_click(x, y):#pour 10x10
    return (x//(WIDTH/NB_CASES)), (y//(HEIGHT/NB_CASES))

fltk.cree_fenetre(WIDTH, HEIGHT)
grille = [[None] * NB_CASES for _ in range(NB_CASES)]
tuiles = reader.cree_dico("fichiers fournis/tuiles/")

while True:
    ev = fltk.donne_ev()
    if ev is not None:
        if fltk.type_ev(ev) == "Quitte":
            break
        elif fltk.type_ev(ev) == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            tuiles_possibles = gestion_truiles.tuiles_possibles(tuiles, grille, detect_case_click(x, y))
            tuiles_possibles_alea = []
            fltk.rectangle(MARGIN, MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN, "black", "lightgrey", 1, "choices_display")
            for i in range(5):
                for j in range(5):
                    tuile = random.choice(tuiles_possibles)
                    while tuile in tuiles_possibles_alea:
                        tuile = random.choice(tuiles_possibles)
                    tuiles_possibles_alea.append(tuile)
                    fltk.image(MARGIN + i*(WIDTH - 2*MARGIN)/5, MARGIN + j*(HEIGHT - 2*MARGIN)/5, tuiles_possibles_alea[-1]["fichier"], (WIDTH - 2*MARGIN)/5 - 10, (HEIGHT - 2*MARGIN)/5 - 10, "nw", tuiles_possibles_alea[-1]["nom"])
    fltk.mise_a_jour()
    