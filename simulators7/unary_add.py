def compute(w: str) -> str:
    """
    Fonction de calcul simple représentant une addition unaire.

    Cette fonction prend une chaîne de la forme '111#11' (où le caractère '#' sépare
    deux nombres en unaire) et retourne leur concaténation, représentant la somme.

    Paramètres :
    ------------
    w : str
        Une chaîne représentant deux nombres en unaire, séparés par '#'

    Retour :
    --------
    str
        La somme des deux parties si le format est correct, sinon 'Erreur'

    Exemple :
    ---------
    >>> compute("111#11")
    '11111'
    """
    if "#" not in w:
        return "Erreur"
    left, right = w.split("#")
    return left + right
