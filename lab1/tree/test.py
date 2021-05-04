from graphviz import Digraph
from tree import createPolishNotation, createTree

regExps = ['(a|b)*abb', 'a*b*(aa*|b)']

ast = Digraph('AST', filename='ast.gv');

def createGraphEdges(root):
    print(root.nodeId,' firstPos:',root.firstPos)
    print(root.nodeId,' lastPos:',root.lastPos)
    print(root.nodeId,' nullable:',root.nullable)
    print('-------------------------------------')

    if root.left != None:
        ast.edge(root.nodeId, root.left.nodeId)
        createGraphEdges(root.left)

    if root.right != None:
        ast.edge(root.nodeId, root.right.nodeId)
        createGraphEdges(root.right)

tree = createTree(regExps[1])
createGraphEdges(tree.root)
ast.render()