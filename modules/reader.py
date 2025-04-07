import os

def cree_dico(chemin):
    list_fichiers = os.listdir(chemin)
    tuiles = []
    for fichier in list_fichiers:
        tuiles.append({"nom": fichier[:-4], "chemin": chemin + fichier})
    return tuiles