def compute(tape: str) -> tuple[str, str]:
    """
    Division euclidienne en unaire : '1111#11' => ('11', '0')  (4 ÷ 2)

    Cette fonction simule la division entière de deux entiers représentés en unaire.
    Le format attendu est une chaîne contenant deux blocs de '1' séparés par un '#'.

    Paramètres :
    ------------
    tape : str
        Chaîne contenant deux entiers en unaire séparés par '#',
        représentant le dividende et le diviseur.

    Retour :
    --------
    tuple[str, str]
        Un tuple (quotient, reste), tous deux sous forme unaire.
        Le reste est retourné sous forme '0' si nul.

    Exceptions :
    ------------
    ValueError :
        Levée si le diviseur est vide (division par zéro).

    Exemples :
    ----------
    >>> compute("1111#11")
    ('11', '0')    # 4 ÷ 2 = 2, reste 0

    >>> compute("111#1")
    ('111', '0')   # 3 ÷ 1 = 3, reste 0

    >>> compute("111#11")
    ('1', '1')     # 3 ÷ 2 = 1, reste 1
    """
    # Séparation du dividende et du diviseur
    dividend, divisor = tape.split('#')
    a = len(dividend)
    b = len(divisor)

    # Gestion du cas interdit : division par zéro
    if b == 0:
        raise ValueError("Division par zéro")

    # Calcul du quotient et du reste
    quotient = a // b
    remainder = a % b

    # Retourne les deux résultats en unaire
    return ('1' * quotient, '1' * remainder if remainder > 0 else '0')
