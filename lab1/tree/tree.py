from treeUtils import multiPriority, expandWithPlus, isSymbol


class Node:
    def __init__(self, symbol):
        self.number = 0
        self.symbol = symbol
        self.parent = None
        self.left = None
        self.right = None
        self.firstPos = set()
        self.lastPos = set()
        self.nullable = False

        self.nodeId = 0

class Tree:
    def __init__(self):
        self.root = None
        # self.nodeStack = []
        # self.nums = 0
        # ноды в порядке следовая по Node.number
        self.numed = {}
        self.followPos = {}


def setFirstLastPos(node):
    if isSymbol(node.symbol):
        node.firstPos.add(node.number)
        node.lastPos.add(node.number)

    elif node.symbol == '+':
        # firstPos
        leftNullable = node.left.nullable
        if leftNullable:
            node.firstPos = node.left.firstPos.union(node.right.firstPos)
        else:
            node.firstPos = node.left.firstPos
        
        # lastPos
        rightNullable = node.right.nullable
        if rightNullable:
            node.lastPos = node.left.lastPos.union(node.right.lastPos)
        else:
            node.lastPos = node.right.lastPos

    elif node.symbol == '|':
        # firstPos
        node.firstPos = node.left.firstPos.union(node.right.firstPos)

        # lastPos
        node.lastPos = node.left.lastPos.union(node.right.lastPos)
    
    elif node.symbol == '*':
        node.firstPos = node.left.firstPos
        node.lastPos = node.left.lastPos


def setNullable(node):
    if isSymbol(node.symbol):
        node.nullable = False

    if node.symbol == '*':
        node.nullable = True

    elif node.symbol == '+':
        rightNullable = node.right.nullable
        leftNullable = node.left.nullable

        node.nullable = rightNullable and leftNullable

    elif node.symbol == '|':
        rightNullable = node.right.nullable
        leftNullable = node.left.nullable

        node.nullable = rightNullable or leftNullable

def setFollowPos(node, tree):
    if node == None:
        return

    if (node.symbol == '*'):
        for pos in node.left.lastPos:
            tree.followPos[str(pos)] = tree.followPos[str(pos)].union(node.left.firstPos)

    elif (node.symbol == '+'):
        for pos in node.left.lastPos:
            tree.followPos[str(pos)] = tree.followPos[str(pos)].union(node.right.firstPos)

    setFollowPos(node.right, tree)
    setFollowPos(node.left, tree)



def checkPriority(op1, op2):
    return multiPriority(op1, op2)

def createPolishNotation(regExp):
    exp = expandWithPlus(regExp)
    exp += '+#'
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
    # <graphviz>
    nodeId = 0 # индекс ноды для graphviz - нужен только для корректной отрисовки дерева
    # </graphviz>

    stack = []
    nodeNum = 1
    tree = Tree()

    exp = createPolishNotation(regExp)

    for i in range(len(exp)):
        if isSymbol(exp[i]):
            symbolNode = Node(exp[i])
            symbolNode.number = nodeNum

            setNullable(symbolNode)
            setFirstLastPos(symbolNode)

            # <graphviz>
            symbolNode.nodeId = symbolNode.symbol + '_' + str(nodeId)
            nodeId += 1
            # </graphviz>

            stack.append(symbolNode)
            tree.numed[nodeNum] = symbolNode.symbol
            tree.followPos[str(nodeNum)] = set()

            nodeNum += 1

        elif exp[i] == '*':
            # создаем ноду операции
            operationNode = Node(exp[i])

            # достаем из стека ноду сверху и связываем их
            childNode = stack.pop()
            operationNode.left = childNode
            childNode.parent = operationNode

            setNullable(operationNode)
            setFirstLastPos(operationNode)

            # <graphviz>
            operationNode.nodeId = operationNode.symbol + '_' + str(nodeId)
            nodeId += 1
            # </graphviz>

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

            setNullable(operationNode)
            setFirstLastPos(operationNode)

            # <graphviz>
            operationNode.nodeId = operationNode.symbol + '_' + str(nodeId)
            nodeId += 1
            # </graphviz>

            # добавляем новую ноду из трех связанных в стек
            stack.append(operationNode)

    root = stack.pop()
    tree.root = root
    setFollowPos(tree.root, tree)
    return tree





