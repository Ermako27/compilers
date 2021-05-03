from treeUtils import multiPriority, expandWithPlus, isSymbol

class Node:
    def __init__(self, symbol):
        self.number = 0
        self.symbol = symbol
        self.parent = None
        self.left = None
        self.right = None
        self.firstPos = {}
        self.lastPos = {}
        self.nullable = False

class Tree:
    def __init__(self):
        self.root = None
        # self.nodeStack = []
        # self.nums = 0
        # ноды в порядке следовая по Node.number
        self.numed = []
        self.followPos = {}





def checkPriority(op1, op2):
    return multiPriority(op1, op2)

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

def createTree(regExp):
    stack = []
    nodeNum = 1
    tree = Tree()

    exp = createPolishNotation(regExp)
    for i in range(len(exp)):
        if isSymbol(exp[i]):
            symbolNode = Node(exp[i])
            symbolNode.number = nodeNum
            nodeNum += 1
            stack.append(symbolNode)
            tree.numed.append(symbolNode)
        elif exp[i] == '*':
            # создаем ноду операции
            operationNode = Node(exp[i])

            # достаем из стека ноду сверху и связываем их
            childNode = stack.pop()
            operationNode.left = childNode
            childNode.parent = operationNode

            # добавляем новую ноду из двух связанных в стек
            stack.append(operationNode)
        else: # сюда попадают любые другие операции
            # создаем ноду операции
            operationNode = Node(exp[i])

            rightChildNode = stack.pop()
            leftChildNode = stack.pop()
    
            operationNode.right = rightChildNode
            operationNode.left = leftChildNode

            rightChildNode.parent = operationNode
            leftChildNode.parent = operationNode

            # добавляем новую ноду из трех связанных в стек
            stack.append(operationNode)
        
    print(stack)

    root = stack.pop()
    tree.root = root
    return tree





