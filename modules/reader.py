import os, json

def cree_dico(chemin):
    """lit le contenu d'un dossier et renvoie une liste de dictionnaire contenant le nom et le chemin de chaque fichier.

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

def save_json(grille, nom_carte):
    """Met a jour le fichier save.json avec la grille et le nom de la carte.

    Args:
        grille (list[list]): grille globale de la carte
        nom_carte (str): nom de la carte
    """
    data = read()
    for d in data:
        if d["nom_carte"] == nom_carte:
            data.remove(d)
    data.append({"grille": grille, "nom_carte": nom_carte})
    writer = open("save.json", "w", encoding="utf-8")
    json.dump(data, writer)
    writer.close()
    
def read():
    """Lit le fichier save.json et renvoie son contenu."""
    reader = open("save.json", "r", encoding="utf-8")
    try:
        data = json.load(reader)
    except json.decoder.JSONDecodeError:
        data = []
    reader.close()
    return data