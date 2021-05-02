regExp = '(a|b)*abb'

def isSymbol(symbol):
    return symbol.isalpha() or symbol.isdigit()

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

def createPolishNotation(regExp):
    exp = regExp #expandWithPlus(expandWithPlus(regExp))
    result = ''
    stack = [] # привет
    for i in range(len(exp)):
        if isSymbol(exp[i]): # Если токен — символ то добавить его в очередь вывод
            # то добавить его в очередь вывод
            result += exp[i]
        elif exp[i] == '(': # Если токен — открывающая скобка
            # то положить его в стек  
            stack.append(exp[i])
        elif exp[i] == ')': # Если токен — закрывающая скобка
            # Пока токен на вершине стека не является открывающей скобкой, перекладывать операторы из стека в выходную очередь.
            while stack[-1] != '(':
                operation = stack.pop()
                result += operation

            # Выкинуть открывающую скобку из стека, но не добавлять в очередь вывода.
            stack.pop()
        else: # Если токен — оператор op1
            # Пока присутствует на вершине стека токен оператор op2, чей приоритет выше или равен приоритету op1
            # op1 - exp[i], op2 - stack[-1]
            while len(stack) != 0 and checkPriority(exp[i], stack[-1]):
                # переложить op2 из стека в выходную очередь
                operation = stack.pop()
                result += operation

            # Положить op1 в стек.
            stack.append(exp[i])
    
    while (len(stack) != 0):
        operation = stack.pop()
        result += operation

    return result

def checkPriority(op1, op2):
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

print(createPolishNotation('(a+b)*(c+d)-e'))
print(createPolishNotation('(8+2*5)/(1+3*2-4)'))
