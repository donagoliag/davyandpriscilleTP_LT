def is_palindrome(w: str) -> bool:
    """
    Vérifie si une chaîne de caractères est un palindrome.

    Un palindrome est une chaîne qui se lit de la même façon
    de gauche à droite et de droite à gauche.

    Exemple :
        - "radar" => True
        - "abba" => True
        - "hello" => False

    Paramètres :
    -----------
    w : str
        La chaîne de caractères à tester.

    Retour :
    --------
    bool
        True si w est un palindrome, False sinon.
    """
    # On convertit la chaîne en liste pour avoir un accès indexé aux caractères
    tape = list(w)

    # Pointeurs de début (gauche) et de fin (droite)
    left = 0
    right = len(tape) - 1

    # On compare les caractères symétriques jusqu'à se croiser
    while left < right:
        if tape[left] != tape[right]:
            return False  # Dès qu'une paire ne correspond pas, ce n'est pas un palindrome
        left += 1
        right -= 1

    return True  # Toutes les paires correspondent, c'est un palindrome

