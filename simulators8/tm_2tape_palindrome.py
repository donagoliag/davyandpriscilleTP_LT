# tm_2tape_palindrome.py
def run(w):
    """
    Fonction simulant une machine de Turing à deux rubans pour vérifier si
    une chaîne de la forme 'mot#mot' est un palindrome (deux parties identiques).
    
    Paramètre :
    - w (str) : chaîne d'entrée contenant exactement un '#' séparant deux parties.
    
    Retour :
    - (bool, list) : un booléen indiquant si la chaîne est valide palindrome,
      et une liste de chaînes décrivant la trace détaillée de l'exécution.
    """
    
    trace = []  # Liste pour stocker la trace des étapes de l'exécution
    
    # Vérification de la présence du symbole '#' obligatoire
    if "#" not in w:
        return False, ["Erreur : # manquant"]
    
    # Séparation de la chaîne en deux parties, avant et après le '#'
    left, right = w.split("#")
    
    # Initialisation des deux rubans
    tape1 = list(w)       # Ruban 1 : contient toute la chaîne d'entrée
    tape2 = list(left)    # Ruban 2 : copie initiale de la partie gauche (avant '#')
    
    # Initialisation des positions des têtes de lecture sur les rubans
    pos1 = 0  # position de la tête sur ruban 1
    pos2 = 0  # position de la tête sur ruban 2
    
    # Ajout des informations initiales dans la trace
    trace.append(f"Initialisation:")
    trace.append(f"Ruban 1: {''.join(tape1)} (position {pos1})")
    trace.append(f"Ruban 2: {''.join(tape2)} (position {pos2})")
    trace.append("---")
    
    # Phase 1 : copie des symboles avant '#' du ruban 1 vers le ruban 2
    while pos1 < len(tape1) and tape1[pos1] != '#':
        trace.append(f"Étape {len(trace)}: Copie '{tape1[pos1]}' du ruban 1 au ruban 2")
        tape2[pos2] = tape1[pos1]  # copie du symbole
        pos1 += 1
        pos2 += 1
        trace.append(f"Ruban 1: {''.join(tape1)} (position {pos1})")
        trace.append(f"Ruban 2: {''.join(tape2)} (position {pos2})")
        trace.append("---")
    
    pos1 += 1  # On saute le symbole '#'
    pos2 = 0   # Retour à la position initiale du ruban 2 pour comparaison
    
    # Phase 2 : comparaison caractère par caractère entre la partie droite et la copie
    result = True  # flag indiquant si les deux parties sont identiques
    
    while pos1 < len(tape1) and pos2 < len(tape2):
        trace.append(f"Étape {len(trace)}: Comparaison '{tape1[pos1]}' (ruban1) et '{tape2[pos2]}' (ruban2)")
        if tape1[pos1] != tape2[pos2]:
            # Si un caractère ne correspond pas, ce n'est pas un palindrome
            result = False
            break
        pos1 += 1
        pos2 += 1
        trace.append(f"Ruban 1: {''.join(tape1)} (position {pos1})")
        trace.append(f"Ruban 2: {''.join(tape2)} (position {pos2})")
        trace.append("---")
    
    # Vérification que les deux parties ont la même longueur
    if pos1 < len(tape1) or pos2 < len(tape2):
        result = False
    
    # Retourne le résultat et la trace d'exécution complète
    return result, trace
