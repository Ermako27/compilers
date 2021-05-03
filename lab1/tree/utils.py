def multiPriority(op1, op2):
    if (op1 == op2):
        return True
    
    if (op1 == '*'):
        return False

    if (op2 == '*'):
        return True

    if (op1 == '+'):
        return False

    if (op2 == '+'):
        return True

    if (op1 == '|'):
        return False
    
    return True

def numberPriority(op1, op2):
    operations = {
        '(': 0,
        ')': 1,
        '+': 2,
        '-': 2,
        '*': 3,
        '/': 3
    }

    op1Priority = operations[op1]
    op2Priority = operations[op2]

    if (op2Priority >= op1Priority):
        return True
    else:
        return False


def expandWithPlus(regExp):
    result = ''
    for i in range(len(regExp) - 1):
        if regExp[i].isalpha():
            if regExp[i + 1].isalpha():
                result += regExp[i] + '+'
            
            if regExp[i + 1] == '(':
                result += regExp[i] + '+'
            
            if regExp[i + 1] == ')':
                result += regExp[i]
            
            if regExp[i + 1] == '*' or regExp[i + 1] == '|':
                result += regExp[i]

        elif regExp[i] == '(':
            result += regExp[i]
        elif regExp[i] == ')':
            if regExp[i + 1].isalpha():
                result += regExp[i] + '+'

            if regExp[i + 1] == '(':
                result += regExp[i] + '+'

            if regExp[i + 1] == '*' or regExp[i + 1] == '|' or  regExp[i + 1] == ')':
                result += regExp[i]
        elif regExp[i] == '*':
            if regExp[i + 1].isalpha() or regExp[i + 1] == '(':
                result += regExp[i] + '+'
            else:
                result += regExp[i]
        elif regExp[i] == '|':
            result += regExp[i]
        
    result += regExp[len(regExp) - 1]
    return result


def isSymbol(symbol):
    if symbol == '#':
        return True

    return symbol.isalpha() or symbol.isdigit()