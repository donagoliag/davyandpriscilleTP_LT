def compute(tape: str) -> str:
    """
    Simule la multiplication unaire : '111#11' => '111111' (3 × 2)
    Multiplie le premier nombre par le nombre de '1' du second
    """
    left, right = tape.split('#')
    multiplicand = len(left)
    multiplier = len(right)
    result = '1' * (multiplicand * multiplier)
    return result