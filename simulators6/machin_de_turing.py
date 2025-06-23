import streamlit as st
class MachineDeTuring:
    def __init__(self, etats, alphabet_entree, alphabet_travail, transitions, etat_initial, etats_finaux, symbole_vide='_'):
        """
        Initialise une machine de Turing avec:
        - etats: ensemble fini d'états (ex: {'q0', 'q1', 'qf'})
        - alphabet_entree: alphabet d'entrée (ex: {'a', 'b'})
        - alphabet_travail: alphabet de travail (inclut alphabet_entree + symboles spéciaux)
        - transitions: dictionnaire des transitions
        - etat_initial: état de départ
        - etats_finaux: états d'acceptation
        - symbole_vide: symbole blanc (par défaut '_')
        """
        self.etats = etats
        self.alphabet_entree = alphabet_entree
        self.alphabet_travail = alphabet_travail
        self.transitions = transitions
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux
        self.symbole_vide = symbole_vide
        self.trace = []
        
        self._valider_machine()

    def _valider_machine(self):
        """Valide la cohérence de la machine."""
        # Validation des états
        assert self.etat_initial in self.etats
        assert self.etats_finaux.issubset(self.etats)
        
        # Validation des alphabets
        assert self.alphabet_entree.issubset(self.alphabet_travail), \
            "L'alphabet d'entrée doit être inclus dans l'alphabet de travail"
        assert self.symbole_vide in self.alphabet_travail, \
            "Le symbole vide doit faire partie de l'alphabet de travail"
            
        # Validation des transitions
        for (etat, symbole), (new_etat, new_symb, dir) in self.transitions.items():
            assert etat in self.etats, f"État {etat} inconnu"
            assert new_etat in self.etats, f"État {new_etat} inconnu"
            assert symbole in self.alphabet_travail, f"Symbole {symbole} non autorisé"
            assert new_symb in self.alphabet_travail, f"Symbole {new_symb} non autorisé"
            assert dir in {'L', 'R', 'S'}, f"Direction {dir} invalide"

    def executer(self, mot):
        """Exécute la machine sur un mot d'entrée"""
        self.trace = []
        
        # Vérification que le mot utilise l'alphabet d'entrée
        if not set(mot).issubset(self.alphabet_entree):
            raise ValueError(f"Le mot contient des symboles non autorisés dans l'alphabet d'entrée: {set(mot) - self.alphabet_entree}")
            
        ruban = list(mot + self.symbole_vide)
        position = 0
        etat_courant = self.etat_initial
        
        while True:
            # Configuration actuelle
            config = {
                "etat": etat_courant,
                "ruban": ''.join(ruban),
                "position": position,
                "symbole_courant": ruban[position] if position < len(ruban) else self.symbole_vide
            }
            self.trace.append(config)
            
            # Condition d'arrêt
            if etat_courant in self.etats_finaux:
                return True
                
            # Transition
            symbole_lu = ruban[position] if position < len(ruban) else self.symbole_vide
            transition = self.transitions.get((etat_courant, symbole_lu))
            
            if transition is None:
                return False
                
            # Mise à jour
            nouvel_etat, nouveau_symbole, direction = transition
            
            # Écriture
            if position < len(ruban):
                ruban[position] = nouveau_symbole
            else:
                ruban.append(nouveau_symbole)
            
            # Déplacement
            if direction == 'L':
                position = max(0, position - 1)
            elif direction == 'R':
                position += 1
            # 'S' ne change pas la position
            
            etat_courant = nouvel_etat

    def afficher_trace(self):
        """Affiche la trace d'exécution"""
        for i, step in enumerate(self.trace):
            ruban = step['ruban']
            pos = step['position']
            print(f"Étape {i}:")
            print(f"État: {step['etat']}")
            print(f"Ruban: {ruban[:pos]}[{ruban[pos] if pos < len(ruban) else '_'}]{ruban[pos+1:]}")
            print("---")