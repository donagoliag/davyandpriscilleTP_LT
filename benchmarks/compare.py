# compare.py
import time
from simulators8.tm_2tape_palindrome import run as run_2tape

def simulate_1tape(w):
    """Version naïve 1 ruban"""
    if "#" not in w: return False
    left, right = w.split("#")
    return left == right

def compare_versions(w):
    """Compare les temps d'exécution"""
    # Version 1 ruban
    start = time.perf_counter()
    result_1tape = simulate_1tape(w)
    time_1tape = (time.perf_counter() - start) * 1000  # en ms
    
    # Version 2 rubans
    start = time.perf_counter()
    result_2tape, _ = run_2tape(w)
    time_2tape = (time.perf_counter() - start) * 1000  # en ms
    
    return {
        "Mot testé": w,
        "Résultat 1 ruban": "Accepté" if result_1tape else "Rejeté",
        "Résultat 2 rubans": "Accepté" if result_2tape else "Rejeté",
        "Temps 1 ruban": f"{time_1tape:.3f} ms",
        "Temps 2 rubans": f"{time_2tape:.3f} ms",
        "Gain relatif": f"{(time_1tape - time_2tape)/time_1tape * 100:.1f}%",
        "Conclusion": "2 rubans plus rapide ✅" if time_2tape < time_1tape else "1 ruban plus rapide ❌"
    }