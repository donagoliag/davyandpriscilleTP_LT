def encode_unary(n: int) -> str:
    return '1' * (n + 1)

def encode_symbol(sym: str) -> str:
    symbol_map = {'a': '1', 'b': '11', 'B': '111'}
    return symbol_map.get(sym, '111')  # Default to blank

def encode_direction(dir: str) -> str:
    return '1' if dir == 'R' else '11'

def encode_transition(q, x, p, y, d) -> str:
    return f"{encode_unary(q)}0{encode_symbol(x)}0{encode_unary(p)}0{encode_symbol(y)}0{encode_direction(d)}"

def encode_all(transitions: list[tuple[int, str, int, str, str]]) -> str:
    return '000'.join(encode_transition(*t) for t in transitions)

def encode_input(word: str) -> str:
    return '0'.join(encode_symbol(c) for c in word)
