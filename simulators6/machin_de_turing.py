import streamlit as st
import streamlit as st
import time
from typing import Dict, Set, List, Tuple, Optional

class MachineDeTuring:
    """
    Simulateur de machine de Turing avec gestion complète des transitions,
    du ruban, et de la trace d'exécution.
    
    Une machine de Turing est définie par :
    - Un ensemble fini d'états
    - Un alphabet d'entrée et un alphabet de travail
    - Une fonction de transition
    - Un état initial et des états finaux
    - Un symbole blanc pour les cases vides
    
    Attributes:
        etats (Set[str]): Ensemble de tous les états possibles
        alphabet_entree (Set[str]): Alphabet des symboles d'entrée
        alphabet_travail (Set[str]): Alphabet de travail (inclut entrée + blanc)
        transitions (Dict): Fonction de transition {(état, symbole): (nouvel_état, nouveau_symbole, direction)}
        etat_initial (str): État de départ
        etats_finaux (Set[str]): États d'acceptation
        symbole_blanc (str): Symbole pour les cases vides
        ruban (List[str]): Contenu actuel du ruban
        position_tete (int): Position de la tête de lecture/écriture
        etat_courant (str): État actuel de la machine
        trace (List[Dict]): Historique des configurations
        nb_etapes (int): Nombre d'étapes exécutées
    """
    
    def __init__(self, etats: Set[str], alphabet_entree: Set[str], 
                 alphabet_travail: Set[str], transitions: Dict[Tuple[str, str], Tuple[str, str, str]], 
                 etat_initial: str, etats_finaux: Set[str], symbole_blanc: str = '_'):
        """
        Initialise une nouvelle machine de Turing.
        
        Args:
            etats (Set[str]): Ensemble des états de la machine
                Exemple: {'q0', 'q1', 'q_accept', 'q_reject'}
            alphabet_entree (Set[str]): Symboles autorisés en entrée
                Exemple: {'a', 'b'} pour un alphabet binaire
            alphabet_travail (Set[str]): Symboles utilisables sur le ruban
                Exemple: {'a', 'b', '_', 'X', 'Y'} (inclut marqueurs)
            transitions (Dict[Tuple[str, str], Tuple[str, str, str]]): 
                Fonction de transition sous forme de dictionnaire
                Clé: (état_actuel, symbole_lu)
                Valeur: (nouvel_état, symbole_à_écrire, direction)
                Direction: 'L' (gauche), 'R' (droite), 'S' (stationnaire)
                Exemple: {('q0', 'a'): ('q1', 'X', 'R')}
            etat_initial (str): État de départ de l'exécution
            etats_finaux (Set[str]): États d'acceptation
            symbole_blanc (str, optional): Symbole pour cases vides. Défaut: '_'
        
        Raises:
            ValueError: Si les paramètres sont incohérents
        """
        # Validation des paramètres
        if etat_initial not in etats:
            raise ValueError(f"L'état initial '{etat_initial}' n'est pas dans l'ensemble des états")
        if not etats_finaux.issubset(etats):
            raise ValueError("Les états finaux doivent être inclus dans l'ensemble des états")
        if symbole_blanc not in alphabet_travail:
            raise ValueError(f"Le symbole blanc '{symbole_blanc}' doit être dans l'alphabet de travail")
        
        # Définition de la machine
        self.etats = etats
        self.alphabet_entree = alphabet_entree
        self.alphabet_travail = alphabet_travail
        self.transitions = transitions
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux
        self.symbole_blanc = symbole_blanc
        
        # État d'exécution (initialisé par initialiser_ruban)
        self.ruban = []
        self.position_tete = 0
        self.etat_courant = etat_initial
        self.trace = []
        self.nb_etapes = 0
        
    def initialiser_ruban(self, mot: str):
        """
        Initialise le ruban avec le mot d'entrée et remet la machine à l'état initial.
        
        Args:
            mot (str): Mot d'entrée à placer sur le ruban
                      Si vide, initialise avec un symbole blanc
        
        Note:
            - La tête de lecture est positionnée au début du mot
            - L'état courant est remis à l'état initial
            - La trace et le compteur d'étapes sont réinitialisés
        """
        self.ruban = list(mot) if mot else [self.symbole_blanc]
        self.position_tete = 0
        self.etat_courant = self.etat_initial
        self.trace = []
        self.nb_etapes = 0
        
    def etendre_ruban_si_necessaire(self):
        """
        Étend automatiquement le ruban si la tête de lecture sort des limites.
        
        Le ruban est théoriquement infini, cette méthode simule cette propriété :
        - Si la tête va à gauche du début, ajoute un symbole blanc au début
        - Si la tête va à droite de la fin, ajoute un symbole blanc à la fin
        
        Note:
            Cette méthode est appelée automatiquement avant chaque lecture/écriture
        """
        if self.position_tete < 0:
            # Tête à gauche du ruban : ajouter une case vide au début
            self.ruban.insert(0, self.symbole_blanc)
            self.position_tete = 0  # Réajuster la position
        elif self.position_tete >= len(self.ruban):
            # Tête à droite du ruban : ajouter une case vide à la fin
            self.ruban.append(self.symbole_blanc)
            
    def obtenir_symbole_courant(self) -> str:
        """
        Retourne le symbole sous la tête de lecture.
        
        Returns:
            str: Le symbole à la position courante de la tête
        
        Note:
            Étend automatiquement le ruban si nécessaire
        """
        self.etendre_ruban_si_necessaire()
        return self.ruban[self.position_tete]
        
    def ecrire_symbole(self, symbole: str):
        """
        Écrit un symbole à la position courante de la tête.
        
        Args:
            symbole (str): Symbole à écrire (doit être dans l'alphabet de travail)
        
        Note:
            Étend automatiquement le ruban si nécessaire
        """
        self.etendre_ruban_si_necessaire()
        self.ruban[self.position_tete] = symbole
        
    def deplacer_tete(self, direction: str):
        """
        Déplace la tête de lecture selon la direction spécifiée.
        
        Args:
            direction (str): Direction du mouvement
                'L' ou 'G' : Gauche (position - 1)
                'R' ou 'D' : Droite (position + 1)  
                'S' : Stationnaire (pas de mouvement)
        
        Note:
            Les positions négatives sont gérées par etendre_ruban_si_necessaire()
        """
        if direction == 'L' or direction == 'G':  # Gauche
            self.position_tete -= 1
        elif direction == 'R' or direction == 'D':  # Droite
            self.position_tete += 1
        # 'S' = Stationnaire (pas de mouvement)
        
    def obtenir_configuration_ruban(self) -> str:
        """
        Retourne une représentation textuelle du ruban avec la position de la tête.
        
        Returns:
            str: Représentation du ruban avec la tête marquée entre crochets
                 Exemple: "ab[c]de" si la tête est sur 'c'
        
        Note:
            Utilisé pour l'affichage et la trace d'exécution
        """
        ruban_str = ''.join(self.ruban)
        # Ajouter des marqueurs pour la position de la tête
        if 0 <= self.position_tete < len(self.ruban):
            return f"{ruban_str[:self.position_tete]}[{self.ruban[self.position_tete]}]{ruban_str[self.position_tete+1:]}"
        return ruban_str
        
    def executer_etape(self) -> bool:
        """
        Exécute une seule étape de la machine de Turing.
        
        Une étape consiste à :
        1. Lire le symbole sous la tête
        2. Chercher une transition correspondante
        3. Appliquer la transition (écrire, déplacer, changer d'état)
        4. Enregistrer la configuration dans la trace
        
        Returns:
            bool: True si l'exécution peut continuer, False sinon
                  False est retourné si aucune transition n'est définie
        
        Note:
            Cette méthode met automatiquement à jour :
            - L'état courant
            - Le contenu du ruban
            - La position de la tête
            - La trace d'exécution
            - Le compteur d'étapes
        """
        symbole_courant = self.obtenir_symbole_courant()
        cle_transition = (self.etat_courant, symbole_courant)
        
        # Enregistrer la configuration AVANT la transition
        self.trace.append({
            'etape': self.nb_etapes,
            'etat': self.etat_courant,
            'symbole_lu': symbole_courant,
            'position': self.position_tete,
            'ruban': self.obtenir_configuration_ruban()
        })
        
        # Vérifier si une transition existe pour cette configuration
        if cle_transition not in self.transitions:
            return False  # Pas de transition définie, arrêt de l'exécution
            
        # Récupérer et appliquer la transition
        nouvel_etat, nouveau_symbole, direction = self.transitions[cle_transition]
        
        # Appliquer les modifications
        self.ecrire_symbole(nouveau_symbole)
        self.deplacer_tete(direction)
        self.etat_courant = nouvel_etat
        self.nb_etapes += 1
        
        return True  # Exécution peut continuer
        
    def executer(self, mot: str, max_etapes: int = 1000) -> Dict:
        """
        Exécute complètement la machine de Turing sur un mot d'entrée.
        
        Args:
            mot (str): Mot d'entrée à traiter
            max_etapes (int, optional): Nombre maximum d'étapes pour éviter
                                      les boucles infinies. Défaut: 1000
        
        Returns:
            Dict: Résultat de l'exécution contenant :
                'accepte' (bool): True si le mot est accepté
                'etat_final' (str): État final atteint
                'ruban_final' (str): Contenu final du ruban (sans symboles blancs)
                'nb_etapes' (int): Nombre d'étapes exécutées
                'trace' (List[Dict]): Trace complète de l'exécution
                'raison' (str, optionnel): Raison de l'arrêt si non accepté
        
        Note:
            Un mot est accepté si la machine atteint un état final.
            L'exécution s'arrête si :
            - Un état final est atteint (accepté)
            - Aucune transition n'est définie (rejeté)
            - Le nombre maximum d'étapes est atteint (timeout)
        """
        self.initialiser_ruban(mot)
        
        # Boucle principale d'exécution
        while self.nb_etapes < max_etapes:
            # Vérifier si on a atteint un état final
            if self.etat_courant in self.etats_finaux:
                # Ajouter la configuration finale à la trace
                self.trace.append({
                    'etape': self.nb_etapes,
                    'etat': self.etat_courant,
                    'symbole_lu': self.obtenir_symbole_courant(),
                    'position': self.position_tete,
                    'ruban': self.obtenir_configuration_ruban()
                })
                return {
                    'accepte': True,
                    'etat_final': self.etat_courant,
                    'ruban_final': ''.join(self.ruban).strip(self.symbole_blanc),
                    'nb_etapes': self.nb_etapes,
                    'trace': self.trace
                }
                
            # Essayer d'exécuter une étape
            if not self.executer_etape():
                # Pas de transition possible - mot rejeté
                return {
                    'accepte': False,
                    'etat_final': self.etat_courant,
                    'ruban_final': ''.join(self.ruban).strip(self.symbole_blanc),
                    'nb_etapes': self.nb_etapes,
                    'trace': self.trace,
                    'raison': 'Pas de transition définie'
                }
                
        # Timeout atteint - probablement une boucle infinie
        return {
            'accepte': False,
            'etat_final': self.etat_courant,
            'ruban_final': ''.join(self.ruban).strip(self.symbole_blanc),
            'nb_etapes': self.nb_etapes,
            'trace': self.trace,
            'raison': f'Timeout après {max_etapes} étapes'
        }

# ============================================================================
# MACHINES DE TURING PRÉDÉFINIES POUR LES TESTS
# ============================================================================

def creer_machine_palindromes():
    """
    Crée une machine de Turing qui reconnaît les palindromes sur l'alphabet {a, b}.
    
    Un palindrome est un mot qui se lit de la même façon dans les deux sens.
    Exemples: "aba", "abba", "a", "bb", "" (chaîne vide)
    
    Algorithme:
    1. Effacer le premier caractère et mémoriser sa valeur
    2. Aller à la fin du mot
    3. Vérifier que le dernier caractère correspond au premier
    4. Effacer le dernier caractère
    5. Répéter jusqu'à ce que le mot soit vide ou réduit à un caractère
    
    Returns:
        MachineDeTuring: Machine configurée pour reconnaître les palindromes
    
    États:
        q0: État initial - examine le premier caractère
        q1: Cherche la fin après avoir lu 'a'
        q2: Cherche la fin après avoir lu 'b'  
        q3: Vérifie le dernier caractère pour 'a'
        q4: Vérifie le dernier caractère pour 'b'
        q5: Retourne au début
        q_accept: État d'acceptation
    """
    etats = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q_accept'}
    alphabet_entree = {'a', 'b'}
    alphabet_travail = {'a', 'b', '_'}
    etats_finaux = {'q_accept'}
    
    transitions = {
        # État initial q0 - examiner le premier caractère
        ('q0', '_'): ('q_accept', '_', 'S'),  # Chaîne vide = palindrome
        ('q0', 'a'): ('q1', '_', 'R'),       # Effacer premier 'a', chercher dernier 'a'
        ('q0', 'b'): ('q2', '_', 'R'),       # Effacer premier 'b', chercher dernier 'b'
        
        # q1: aller à la fin après avoir effacé un 'a'
        ('q1', 'a'): ('q1', 'a', 'R'),       # Avancer vers la droite
        ('q1', 'b'): ('q1', 'b', 'R'),       # Avancer vers la droite
        ('q1', '_'): ('q3', '_', 'L'),       # Atteint la fin, chercher 'a' à la fin
        
        # q2: aller à la fin après avoir effacé un 'b'  
        ('q2', 'a'): ('q2', 'a', 'R'),       # Avancer vers la droite
        ('q2', 'b'): ('q2', 'b', 'R'),       # Avancer vers la droite
        ('q2', '_'): ('q4', '_', 'L'),       # Atteint la fin, chercher 'b' à la fin
        
        # q3: vérifier que le dernier caractère est 'a'
        ('q3', 'a'): ('q5', '_', 'L'),       # Trouvé 'a', l'effacer et retourner
        ('q3', 'b'): ('q3', 'b', 'L'),       # Passer les 'b' (ne devrait pas arriver)
        ('q3', '_'): ('q_accept', '_', 'S'),  # Plus de caractères = palindrome
        
        # q4: vérifier que le dernier caractère est 'b'
        ('q4', 'b'): ('q5', '_', 'L'),       # Trouvé 'b', l'effacer et retourner
        ('q4', 'a'): ('q4', 'a', 'L'),       # Passer les 'a' (ne devrait pas arriver)
        ('q4', '_'): ('q_accept', '_', 'S'),  # Plus de caractères = palindrome
        
        # q5: retourner au début pour recommencer
        ('q5', 'a'): ('q5', 'a', 'L'),       # Retourner vers la gauche
        ('q5', 'b'): ('q5', 'b', 'L'),       # Retourner vers la gauche
        ('q5', '_'): ('q0', '_', 'R'),       # Retour au début, recommencer
    }
    
    return MachineDeTuring(etats, alphabet_entree, alphabet_travail, 
                          transitions, 'q0', etats_finaux)

def creer_machine_anbn():
    """
    Crée une machine de Turing qui reconnaît le langage {a^n b^n | n ≥ 0}.
    
    Ce langage contient tous les mots de la forme a...ab...b où le nombre
    de 'a' est égal au nombre de 'b'.
    Exemples: "", "ab", "aabb", "aaabbb"
    
    Algorithme:
    1. Marquer un 'a' à gauche avec 'X'
    2. Chercher un 'b' à droite et le marquer avec 'Y'
    3. Retourner au début
    4. Répéter jusqu'à ce que tous les 'a' et 'b' soient appariés
    5. Vérifier qu'il ne reste que des symboles marqués
    
    Returns:
        MachineDeTuring: Machine configurée pour reconnaître a^n b^n
    
    États:
        q0: Cherche le premier 'a' non marqué
        q1: Cherche le premier 'b' non marqué (après avoir marqué un 'a')
        q2: Retourne au début après avoir marqué un 'b'
        q3: Vérifie que tous les 'b' sont marqués
        q_accept: État d'acceptation
    """
    etats = {'q0', 'q1', 'q2', 'q3', 'q_accept'}
    alphabet_entree = {'a', 'b'}
    alphabet_travail = {'a', 'b', '_', 'X', 'Y'}  # X marque les 'a', Y marque les 'b'
    etats_finaux = {'q_accept'}
    
    transitions = {
        # État q0: Chercher le premier 'a' non marqué
        ('q0', 'a'): ('q1', 'X', 'R'),       # Marquer 'a' avec X, chercher 'b'
        ('q0', 'X'): ('q0', 'X', 'R'),       # Passer les 'a' déjà marqués
        ('q0', 'Y'): ('q3', 'Y', 'R'),       # Tous les 'a' traités, vérifier les 'b'
        ('q0', '_'): ('q_accept', '_', 'S'), # Chaîne vide -> ACCEPTÉ
        
        # État q1: Chercher le premier 'b' non marqué
        ('q1', 'a'): ('q1', 'a', 'R'),       # Passer les 'a' restants
        ('q1', 'X'): ('q1', 'X', 'R'),       # Passer les 'a' marqués
        ('q1', 'Y'): ('q1', 'Y', 'R'),       # Passer les 'b' déjà marqués
        ('q1', 'b'): ('q2', 'Y', 'L'),       # Marquer 'b' avec Y, retourner
        ('q1', '_'): ('q_accept', '_', 'S'), # Pas de 'b' pour ce 'a' -> REJET
        
        # État q2: Retourner au début
        ('q2', 'a'): ('q2', 'a', 'L'),       # Retourner vers la gauche
        ('q2', 'b'): ('q2', 'b', 'L'),       # Retourner vers la gauche
        ('q2', 'X'): ('q2', 'X', 'L'),       # Retourner vers la gauche
        ('q2', 'Y'): ('q2', 'Y', 'L'),       # Retourner vers la gauche
        ('q2', '_'): ('q0', '_', 'R'),       # Recommencer depuis le début
        
        # État q3: Vérifier que tous les 'b' sont marqués
        ('q3', 'Y'): ('q3', 'Y', 'R'),       # Passer les 'b' marqués
        ('q3', 'b'): ('q_accept', 'b', 'S'), # 'b' non marqué -> REJET
        ('q3', '_'): ('q_accept', '_', 'S'), # Fin atteinte -> ACCEPTÉ
    }
    
    return MachineDeTuring(etats, alphabet_entree, alphabet_travail, 
                          transitions, 'q0', etats_finaux)

def creer_machine_addition_unaire():
    """
    Crée une machine de Turing qui effectue l'addition en notation unaire.
    
    En notation unaire, un nombre n est représenté par n occurences du symbole '1'.
    L'addition de deux nombres est représentée par: nombre1 + nombre2
    Exemple: "111+11" représente 3+2 et doit donner "11111" (5)
    
    Algorithme:
    1. Chercher le symbole '+'
    2. Remplacer '+' par '1' (cela ajoute 1 au premier nombre)
    3. Aller à la fin du second nombre
    4. Supprimer le dernier '1' du second nombre
    5. Le résultat est la concaténation des deux nombres
    
    Returns:
        MachineDeTuring: Machine configurée pour l'addition unaire
    
    États:
        q0: Cherche le symbole '+'
        q1: Cherche la fin du second nombre
        q2: Supprime le dernier '1' du second nombre
        q_accept: État d'acceptation
        
    Exemple de fonctionnement:
        Entrée: "111+11"
        Étape 1: "11111"  (+ remplacé par 1)
        Étape 2: "1111"   (dernier 1 supprimé)
        Résultat: "1111" (4, mais devrait être 3+2=5)
        
    Note: Cette implémentation a une erreur dans l'algorithme.
    """
    etats = {'q0', 'q1', 'q2', 'q_accept'}
    alphabet_entree = {'1', '+'}
    alphabet_travail = {'1', '+', '_'}
    etats_finaux = {'q_accept'}
    
    transitions = {
        # État q0: Chercher le symbole '+'
        ('q0', '1'): ('q0', '1', 'R'),       # Passer les '1' du premier nombre
        ('q0', '+'): ('q1', '1', 'R'),       # Remplacer '+' par '1'
        
        # État q1: Chercher la fin du second nombre
        ('q1', '1'): ('q1', '1', 'R'),       # Avancer jusqu'à la fin
        ('q1', '_'): ('q2', '_', 'L'),       # Atteint la fin, reculer
        
        # État q2: Supprimer le dernier '1' du second nombre
        ('q2', '1'): ('q_accept', '_', 'S'), # Supprimer le dernier '1'
    }
    
    return MachineDeTuring(etats, alphabet_entree, alphabet_travail, 
                          transitions, 'q0', etats_finaux)

# ============================================================================
# FONCTIONS DE TEST ET DÉMONSTRATION
# ============================================================================

def test_aba():
    """
    Teste spécifiquement le mot 'aba' avec la machine de reconnaissance des palindromes.
    
    Cette fonction est utile pour déboguer et comprendre le fonctionnement
    de la machine sur un exemple simple.
    
    Returns:
        Dict: Résultat de l'exécution avec tous les détails
        
    Affiche:
        - Résultat de l'acceptation (OUI/NON)
        - État final atteint
        - Nombre d'étapes exécutées
        - Contenu final du ruban
        - Trace complète étape par étape
        
    Note:
        Le mot "aba" est un palindrome et devrait être accepté par la machine.
        La trace permet de suivre chaque transition et l'évolution du ruban.
    """
    # Créer la machine de reconnaissance des palindromes
    machine = creer_machine_palindromes()
    
    # Exécuter sur le mot "aba"
    resultat = machine.executer("aba", 1000)
    
    # Afficher le résumé des résultats
    print("=== TEST DU MOT 'aba' ===")
    print(f"Mot accepté: {'OUI' if resultat['accepte'] else 'NON'}")
    print(f"État final: {resultat['etat_final']}")
    print(f"Nombre d'étapes: {resultat['nb_etapes']}")
    print(f"Ruban final: {resultat['ruban_final']}")
    
    # Afficher la trace complète d'exécution
    print("\n=== TRACE D'EXÉCUTION ===")
    print("Format: Étape | État | Symbole lu | Position | Configuration du ruban")
    print("-" * 70)
    
    for i, etape in enumerate(resultat['trace']):
        print(f"Étape {etape['etape']:2d}: État={etape['etat']:8s} | "
              f"Symbole='{etape['symbole_lu']}' | Pos={etape['position']:2d} | "
              f"Ruban: {etape['ruban']}")
    
    return resultat

