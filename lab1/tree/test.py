from graphviz import Digraph
from tree import createPolishNotation, createTree

regExps = ['(a|b)*abb', 'a*b*(aa*|b)']

ast = Digraph('AST', filename='ast.gv');

def createGraphEdges(root, mokId):
    if root.right != None:
        edge1 = root.symbol + str(mokId)
        mokId += 1
        edge2 = root.right.symbol  + str(mokId)
        mokId += 1

        ast.edge(edge1, edge2)
        createGraphEdges(root.right, mokId)
        
    
    if root.left != None:
        edge1 = root.symbol + str(mokId)
        mokId += 1
        edge2 = root.left.symbol + str(mokId)
        mokId += 1

        ast.edge(edge1, edge2)
        createGraphEdges(root.left, mokId)

# print(createPolishNotation(regExps[0]))
# print('------------------------')
# print(createPolishNotation(regExps[1]))

tree = createTree(regExps[1])
createGraphEdges(tree.root, 0)
print(ast.source)
ast.render()