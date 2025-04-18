import os

def cree_dico(chemin):
    """lit le contenu d'un dossier et renvoie un dictionnaire contenant le nom et le chemin de chaque fichier.

    Args:
        chemin (str): chemin du dossier à lire

    Returns:
        list[dict]: liste de dictionnaires contenant le nom et le chemin de chaque fichier
    """
    list_fichiers = os.listdir(chemin)
    tuiles = []
    for fichier in list_fichiers:
        tuiles.append({"nom": fichier[:-4], "chemin": chemin + fichier})
    return tuiles