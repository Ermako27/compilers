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

def printFollowPos(tree):
    followPosLen = len(tree.followPos)
    print('\n\n\nFollowPos:')
    print('----------------------')
    for key in tree.followPos.keys():
        print('{0} : {1}'.format(key, tree.followPos[key]))

tree = createTree(regExps[1])
createGraphEdges(tree.root)
printFollowPos(tree)
ast.render()