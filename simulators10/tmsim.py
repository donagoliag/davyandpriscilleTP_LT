from collections import deque
import time

class NondeterministicTuringMachine:
    """
    Classe représentant une machine de Turing non déterministe (MTND).

    Cette machine explore plusieurs configurations possibles à chaque étape,
    en utilisant une approche par parcours en largeur (BFS) via une file (deque).

    Attributs :
    -----------
    transitions : dict
        Dictionnaire des transitions au format (état, symbole) → liste de (nouvel état, symbole écrit, direction)
    start_state : str
        État initial (par défaut 'q0')
    accept_states : set
        États d’acceptation (par défaut {'q_accept'})
    max_steps : int
        Nombre maximal de configurations explorées
    paths_explored : int
        Nombre de chemins explorés lors de la simulation
    """

    def __init__(self, transitions, start_state='q0', accept_states=None):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states or ['q_accept'])
        self.max_steps = 1000
        self.paths_explored = 0

    def simulate(self, input_tape):
        """
        Simule la MTND sur un mot d’entrée.

        Paramètres :
        -----------
        input_tape : str
            Le mot à analyser (bande d’entrée)

        Retour :
        --------
        dict : {
            'accepted_paths': liste des chemins menant à l'acceptation,
            'paths_explored': nombre total de chemins explorés,
            'timeout': booléen indiquant un arrêt par dépassement de max_steps
        }
        """
        if input_tape is None:
            input_tape = ''

        # État initial de la file (état, bande, tête, historique)
        initial_config = (
            self.start_state,
            list(input_tape),
            0,
            []
        )
        queue = deque([initial_config])

        self.paths_explored = 0
        accepted_paths = []

        while queue and self.paths_explored < self.max_steps:
            state, tape, head, path = queue.popleft()
            self.paths_explored += 1

            if state in self.accept_states:
                accepted_paths.append(path + [self._config(state, tape, head)])
                continue

            # Gérer dépassements hors limites
            if head < 0:
                tape.insert(0, '_')
                head = 0
            elif head >= len(tape):
                tape.append('_')

            current_symbol = tape[head]

            # Transitions possibles à partir de l'état actuel
            for new_state, write_sym, direction in self.transitions.get((state, current_symbol), []):
                new_tape = tape.copy()
                new_tape[head] = write_sym
                new_head = head + (1 if direction == 'R' else -1)
                new_path = path + [self._config(state, tape, head)]
                queue.append((new_state, new_tape, new_head, new_path))

        return {
            'accepted_paths': accepted_paths,
            'paths_explored': self.paths_explored,
            'timeout': len(queue) > 0
        }

    def _config(self, state, tape, head):
        """
        Représente une configuration de la machine sous forme lisible.

        Exemple : "q0|0101[1]0"
        """
        symbol = tape[head] if 0 <= head < len(tape) else '_'
        left = ''.join(tape[:head])
        right = ''.join(tape[head+1:])
        return f"{state}|{left}[{symbol}]{right}"


class DeterministicTuringMachine:
    """
    Classe représentant une machine de Turing déterministe (MTD).

    À chaque configuration, une seule transition est possible.
    L’exécution suit un chemin unique jusqu’à l’acceptation, l’échec ou le dépassement de pas.

    Attributs :
    -----------
    transitions : dict
        Transitions au format (état, symbole) → (nouvel état, symbole écrit, direction)
    start_state : str
        État de départ
    accept_states : set
        États d'acceptation
    """

    def __init__(self, transitions, start_state='q0', accept_states=None):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = set(accept_states or ['q_accept'])

    def simulate(self, input_tape):
        """
        Simule la machine déterministe sur le mot donné.

        Retourne :
        ----------
        dict : {
            'path': liste des configurations successives,
            'error': (optionnel) si arrêt prématuré,
            'timeout': (optionnel) si boucle infinie
        }
        """
        tape = list(input_tape)
        state = self.start_state
        head = 0
        path = []

        for _ in range(1000):
            path.append(self._config(state, tape, head))

            if state in self.accept_states:
                return {'path': path}

            # Étendre le ruban si nécessaire
            if head < 0:
                tape.insert(0, '_')
                head = 0
            elif head >= len(tape):
                tape.append('_')

            current_symbol = tape[head]
            transition = self.transitions.get((state, current_symbol))

            if not transition:
                return {'path': path, 'error': 'No transition'}

            state, write_sym, direction = transition
            tape[head] = write_sym
            head += 1 if direction == 'R' else -1

        return {'timeout': True, 'path': path}

    def _config(self, state, tape, head):
        """
        Génère une chaîne lisible représentant l’état courant de la machine.
        """
        symbol = tape[head] if 0 <= head < len(tape) else '_'
        left = ''.join(tape[:head]) if head > 0 else ''
        right = ''.join(tape[head+1:]) if head+1 < len(tape) else ''
        return f"{state}|{left}[{symbol}]{right}"
