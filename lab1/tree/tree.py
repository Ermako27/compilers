from utils import multiPriority, expandWithPlus, isSymbol

def createPolishNotation(regExp):
    exp = expandWithPlus(regExp)
    exp += '+#'
    print('expanded:', exp)
    result = ''
    stack = []
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
    return multiPriority(op1, op2)
