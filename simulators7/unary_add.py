def compute(w: str) -> str:
    if "#" not in w: return "Erreur"
    left, right = w.split("#")
    return left + right
