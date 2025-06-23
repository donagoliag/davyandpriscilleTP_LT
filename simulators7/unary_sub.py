def compute(w: str) -> str:
    """
    Soustraction en unaire : calcule max(len(left) - len(right), 0)

    Cette fonction prend une chaîne de la forme '111#11', représentant
    deux entiers en unaire séparés par un '#', et retourne leur
    différence (tronquée à zéro si négative), toujours en unaire.

    Paramètres :
    ------------
    w : str
        Chaîne contenant deux entiers unaire séparés par '#'.

    Retour :
    --------
    str
        Résultat de la soustraction en unaire, ou 'Erreur' si le format est incorrect.

    Exemple :
    ---------
    >>> compute("1111#11")
    '11'

    >>> compute("11#1111")
    '0'

    >>> compute("111")
    'Erreur'
    """
    if "#" not in w:
        return "Erreur"

    # Divise la chaîne en deux parties (nombres) au niveau du '#'.
    left, right = w.split('#')

    # Calcule la différence des longueurs (valeurs en unaire), tronquée à 0 si négative.
    result = max(len(left) - len(right), 0)

    # Retourne une chaîne de '1's correspondant au résultat, ou '0' si le résultat est 0.
    return '1' * result if result > 0 else '0'
