class MultiTapeTuringMachine:
    def __init__(self, k, transitions, start_state='q0', accept_states=None):
        """
        Initialise une machine de Turing à k rubans.

        - k : nombre de rubans
        - transitions : dictionnaire de transitions {(état, symbole1, ..., symbole_k): (nouvel_état, [nouv_symb], [directions])}
        - start_state : état initial (par défaut 'q0')
        - accept_states : liste des états d'acceptation (par défaut ['q_accept'])
        """
        self.k = k
        self.transitions = transitions
        self.state = start_state
        self.accept_states = set(accept_states or ['q_accept'])
        self.tapes = [['B'] for _ in range(k)]  # chaque ruban commence avec un blanc
        self.heads = [0 for _ in range(k)]      # tête de lecture initialisée à 0 pour chaque ruban
        self.trace = []

    def initialize_tape(self, tape_index, content):
        """
        Initialise le contenu d'un ruban (indexé de 0 à k-1).

        - tape_index : index du ruban à initialiser
        - content : chaîne de caractères représentant le contenu du ruban
        """
        self.tapes[tape_index] = list(content) if isinstance(content, str) else content
        self.heads[tape_index] = 0

    def step(self):
        """
        Effectue une seule transition si possible.
        Retourne False si aucune transition applicable.
        """
        # Lire les symboles sous chaque tête
        current_syms = tuple(
            self.tapes[i][self.heads[i]] if 0 <= self.heads[i] < len(self.tapes[i]) else 'B'
            for i in range(self.k)
        )
        key = (self.state,) + current_syms

        if key not in self.transitions:
            return False  # Aucune transition applicable

        new_state, new_syms, directions = self.transitions[key]

        # Écriture et déplacement pour chaque ruban
        for i in range(self.k):
            if 0 <= self.heads[i] < len(self.tapes[i]):
                self.tapes[i][self.heads[i]] = new_syms[i]
            else:
                self.tapes[i].append(new_syms[i])  # si la tête est hors du ruban

            if directions[i] == 'R':
                self.heads[i] += 1
                if self.heads[i] >= len(self.tapes[i]):
                    self.tapes[i].append('B')  # prolonger le ruban
            elif directions[i] == 'L':
                self.heads[i] = max(0, self.heads[i] - 1)
            # Si direction == 'S' → ne rien faire

        self.state = new_state
        self.trace.append(self.snapshot())
        return True

    def run(self, max_steps=1000):
        """
        Exécute la machine jusqu'à acceptation ou blocage.

        - max_steps : limite de sécurité
        - Retourne True si acceptée, False sinon
        """
        self.trace.append(self.snapshot())
        for _ in range(max_steps):
            if self.state in self.accept_states:
                return True
            if not self.step():
                return False
        return False  # Timeout

    def snapshot(self):
        """
        Retourne une chaîne représentant l'état actuel de la machine :
        - État courant
        - Rubans avec position de la tête
        """
        return f"{self.state} | " + " || ".join(
            "".join(self.tapes[i])[:30] + f" (H{self.heads[i]})" for i in range(self.k)
        )
