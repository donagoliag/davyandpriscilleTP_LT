def compute(tape: str) -> tuple[str, str]:
    """
    Simule la division euclidienne unaire : '1111#11' => (quotient='11', reste='') (4 ÷ 2)
    Retourne un tuple (quotient, reste), tous deux en unaire
    """
    dividend, divisor = tape.split('#')
    a = len(dividend)
    b = len(divisor)
    if b == 0:
        raise ValueError("Division par zéro")
    quotient = a // b
    remainder = a % b
    return ('1' * quotient, '1' * remainder if remainder > 0 else '0')
