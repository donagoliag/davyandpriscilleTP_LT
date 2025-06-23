class UniversalTuringMachine:
    """
    Une machine de Turing universelle simple, interprétant une machine encodée en unaire (avec séparateurs binaires).
    
    Paramètres :
    ------------
    transition_code : str
        Code unaire représentant les transitions de la machine simulée (encodage spécifique avec '0' et '000' comme séparateurs).
    input_code : str
        Ruban d’entrée encodé en unaire (liste de symboles séparés par '0').
    accept_states : list
        États d’acceptation (par défaut : ['111'] qui correspond à q3 si q0 = '1', q1 = '11', etc.).
    """
    
    def __init__(self, transition_code: str, input_code: str, accept_states=['111']):
        self.transitions = self.parse_transitions(transition_code)  # Dictionnaire des transitions
        self.tape = self.decode_input(input_code)                   # Ruban initial
        self.state = '1'                                            # État initial q0 → '1'
        self.head = 0                                               # Position de la tête de lecture
        self.blank = 'B'                                            # Symbole blanc par défaut
        self.accept_states = accept_states

    def decode_unary(self, code):
        """Décode un entier encodé unairement. Ex: '111' → 3"""
        return len(code)

    def parse_transitions(self, code: str):
        """
        Décode les transitions encodées comme suit :
        Chaque transition est séparée par '000'.
        Chaque élément d’une transition est séparé par un seul '0'.
        Format attendu : q0 0 sym 0 q1 0 new_sym 0 move
        Exemple : '1 0 1 0 11 0 1 0 1' → (q0, '1') → (q1, '1', 'R')
        """
        transitions = {}
        for raw in code.split('000'):
            if not raw.strip():
                continue
            parts = raw.split('0')
            if len(parts) != 5:
                raise ValueError(f"Bad transition: {raw}")
            q, sym, p, new_sym, move = parts
            key = (q, sym)
            value = (p, new_sym, 'R' if move == '1' else 'L')  # On encode la direction : '1' = droite
            transitions[key] = value
        return transitions

    def decode_input(self, code: str):
        """
        Décode la bande d’entrée :
        Ex: '1 0 1 0 11' → ['1', '1', '11'] (3 symboles unairement encodés)
        """
        parts = code.split('0')
        return parts if parts else []

    def step(self):
        """
        Effectue une seule transition. Renvoie False si aucune règle n’est applicable (arrêt).
        Gère l’élargissement du ruban si la tête sort de ses bornes.
        """
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank)

        current_sym = self.tape[self.head]
        key = (self.state, current_sym)

        if key not in self.transitions:
            return False  # Aucun mouvement possible → arrêt

        next_state, write_sym, direction = self.transitions[key]
        self.tape[self.head] = write_sym
        self.state = next_state
        self.head += 1 if direction == 'R' else -1
        return True

    def run(self, max_steps=1000):
        """
        Exécute la machine jusqu’à acceptation, blocage ou dépassement de pas.

        Retour :
        --------
        bool : True si acceptée, False sinon (rejet ou timeout)
        """
        for _ in range(max_steps):
            if self.state in self.accept_states:
                return True
            if not self.step():
                return False
        return False  # arrêt forcé (timeout)

    def print_tape(self):
        """
        Affiche l’état actuel du ruban avec un curseur ^ indiquant la position de la tête.
        """
        tape_str = ''.join(self.tape)
        head_marker = ' ' * self.head + '^'
        print(tape_str)
        print(head_marker)
