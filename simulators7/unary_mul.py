def compute(tape: str) -> str:
    """
    Multiplie deux entiers en unaire : '111#11' => '111111' (3 × 2 = 6)

    Cette fonction simule une multiplication unaire. Le format attendu est une
    chaîne contenant deux entiers en unaire séparés par un caractère '#'.

    Paramètres :
    ------------
    tape : str
        Chaîne contenant deux blocs de '1', séparés par un '#', représentant
        deux entiers à multiplier.

    Retour :
    --------
    str
        Résultat de la multiplication en unaire (une chaîne de '1'),
        ou génère une exception si le format est invalide.

    Exemple :
    ---------
    >>> compute("111#11")
    '111111'   # 3 × 2 = 6

    >>> compute("1#1111")
    '1111'     # 1 × 4 = 4
    """
    # Sépare les deux opérandes autour du séparateur '#'
    left, right = tape.split('#')

    # Calcule le produit des longueurs (valeurs unaire)
    multiplicand = len(left)
    multiplier = len(right)

    # Construit le résultat : une chaîne contenant (multiplicand × multiplier) fois '1'
    result = '1' * (multiplicand * multiplier)
    return result
