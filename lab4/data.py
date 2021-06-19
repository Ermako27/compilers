MARKER = '$'

# {'xor': 0, 'or': 0, 'and': 0, '/>': 1, '<': 1, '<=': 1, '>=': 1, '>': 1, '=': 1, '+"': 2, '-"': 2, '&': 2, "+'": 3, "-'": 3, 'rem': 4, 'mod': 4, '*': 4, '/': 4, 'abs': 5, '**': 5, 'not': 5}
precedence = {op: p for p, ops in enumerate(reversed([
    {'**', 'abs', 'not'},
    {'*', '/', 'mod', 'rem'},
    {'+\'', '-\''},
    {'+"', '-"', '&'},
    {'<', '<=', '=', '/>', '>', '>='},
    {'and', 'or', 'xor'},
])) for op in ops}

prefix = {'abs', 'not', '+\'', '-\''}

# {'e', 'i', 'k', 'm', 'r', 't', 'a', 'h', 'l', 'c', 'y', 'w', 'x', 'j', 'b', 's', 'v', 'f', 'n', 'q', 'u', 'p', 'd', 'o', 'g', 'z'}
variables = {chr(i) for i in range(ord('a'), ord('z') + 1)}

# {'7', '3', '8', '5', '9', '0', '1', '4', '6', '2'}
constants = {chr(i) for i in range(ord('0'), ord('9') + 1)}

all_tokens = set(precedence) | variables | constants | {'(', ')', MARKER}
