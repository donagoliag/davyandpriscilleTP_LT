def run(input_str):
    """
    Simule une machine de Turing à 3 rubans pour trier une séquence d'entiers.

    - Ruban 1 : contient les nombres en entrée
    - Ruban 2 : ruban de travail temporaire
    - Ruban 3 : ruban de sortie triée

    Paramètre:
        input_str (str): chaîne de caractères contenant les entiers séparés par des espaces

    Retour:
        tuple (list, list): (résultat trié, trace détaillée des opérations)
    """
    try:
        # Conversion de la chaîne en liste d'entiers
        numbers = list(map(int, input_str.strip().split()))
    except ValueError:
        return [], ["Erreur: Entrez des nombres séparés par des espaces (ex: '5 2 7 1')"]

    trace = []

    # Initialisation des rubans
    tape1 = numbers.copy()  # Entrée
    tape2 = []              # Ruban de travail
    tape3 = []              # Ruban de sortie (triée)

    trace.append("Initialisation:")
    trace.append(f"Ruban 1 (entrée): {tape1}")
    trace.append(f"Ruban 2 (travail): {tape2}")
    trace.append(f"Ruban 3 (sortie): {tape3}")
    trace.append("---")

    # Algorithme de tri par sélection simulé via les rubans
    while tape1:
        # Étape 1 : Trouver le minimum sur ruban 1
        min_val = min(tape1)
        trace.append(f"Trouver le minimum: {min_val}")

        tape2 = []  # Réinitialisation du ruban 2
        found_min = False

        # Étape 2 : Séparer le minimum des autres éléments
        for num in tape1:
            if num == min_val and not found_min:
                tape3.append(num)  # Écrire sur ruban 3
                found_min = True
                trace.append(f"Déplacer {num} vers ruban 3 (sortie)")
            else:
                tape2.append(num)  # Garder les autres sur ruban 2
                trace.append(f"Déplacer {num} vers ruban 2 (travail)")

        # Étape 3 : Préparer la prochaine itération
        tape1, tape2 = tape2, []

        # Trace intermédiaire
        trace.append("État après cette itération:")
        trace.append(f"Ruban 1: {tape1}")
        trace.append(f"Ruban 2: {tape2}")
        trace.append(f"Ruban 3: {tape3}")
        trace.append("---")

    return tape3, trace
