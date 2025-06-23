def compute(w: str) -> str:
    if "#" not in w: return "Erreur"
    # Divise la chaîne en deux parties (nombres) au niveau du '#'.
    left, right = w.split('#')
    # Calcule la différence des longueurs (valeurs en unaire), assure que le résultat est >= 0.
    result = max(len(left) - len(right), 0)
    # Retourne une chaîne de '1's correspondant au résultat, ou '0' si le résultat est 0.
    return '1' * result if result > 0 else '0'
