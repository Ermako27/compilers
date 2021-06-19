from data import MARKER, all_tokens, variables, constants, precedence, prefix

def make_relations(tokens, variables, constants, prefix, precedence):
    right_associative = {'**'}

    relations = {t: {t: None for t in tokens} for t in tokens}

    relations['('][')'] = '='

    relations['$']['('] = relations['(']['('] = '<'
    relations[')']['$'] = relations[')'][')'] = '>'

    for thing in variables | constants:
        relations['$'][thing] = relations['('][thing] = '<'
        relations[thing]['$'] = relations[thing][')'] = '>'

    for op in precedence:
        relations[op]['$'] = '>'
        relations['$'][op] = '<'

        relations[op]['('] = relations['('][op] = '<'
        relations[op][')'] = relations[')'][op] = '>'

        for thing in variables | constants:
            relations[op][thing] = '<'
            relations[thing][op] = '>'

        if op in prefix:
            for op2 in precedence:
                relations[op2][op] = '<'
                if precedence[op] > precedence[op2]:
                    relations[op][op2] = '>'
                else:
                    relations[op][op2] = '<'
        else:
            for op2 in precedence:
                if precedence[op] < precedence[op2] or precedence[op] == precedence[op2] and op in right_associative and op2 in right_associative:
                    relations[op][op2] = '<'
                    continue
                if precedence[op] > precedence[op2] or precedence[op] == precedence[op2] and op not in right_associative and op2 not in right_associative:
                    relations[op][op2] = '>'
                    continue

    return relations


class ParseResult:
    def __init__(self, is_correct, result):
        self.is_correct = is_correct
        self.result = result

    def __repr__(self):
        return self.result


def parse(tokens, all_tokens, relations):
    tokens = enumerate(tokens + [MARKER])

    result = []
    next_token_no, next_token = next(tokens)
    stack_tail, stack_head = [], MARKER
    while True:
        if next_token in all_tokens:
            if stack_head == MARKER and next_token == MARKER:
                break

            relation = relations[stack_head][next_token]

            if relation in ('<', '='): # перенос
                stack_tail.append(stack_head)
                stack_head = next_token
                next_token_no, next_token = next(tokens)
                continue
            if relation == '>': # свертка
                while True:
                    if stack_head not in ('(', ')'):
                        result.append(stack_head)
                    old_stack_head = stack_head
                    stack_head = stack_tail.pop()
                    if relations[stack_head][old_stack_head] == '<':
                        break
                continue

        return ParseResult(False, f"Error in {next_token_no} token")

    return ParseResult(True, " ".join(result))

if __name__ == "__main__":
    relations = make_relations(all_tokens, variables, constants, prefix, precedence)
    print(relations)
    #input('Input sequence separate by space: ').strip().split()
    tokens = "( a mod b ) & c".strip().split()
    print(parse(tokens, all_tokens, relations))