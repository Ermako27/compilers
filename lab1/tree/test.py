from graphviz import Digraph
from tree import createPolishNotation, createTree
from dfa import createDfa

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
    print('\n\n\nFollowPos:')
    print('----------------------')
    for key in tree.followPos.keys():
        print('{0} : {1}'.format(key, tree.followPos[key]))

def printNumed(tree):
    numedLen = len(tree.numed)
    print('\n\n\nNumed:')
    print('----------------------')
    for key in tree.numed.keys():
        print('{0}: {1}'.format(key, tree.numed[key]))

def printDfaStates(dfa):
    print('\n\n\nDfa states:')
    print('----------------------')
    for state in dfa.states:
        print(state.positions)

tree = createTree(regExps[1])
createGraphEdges(tree.root)
printFollowPos(tree)
printNumed(tree)
ast.render()

dfa = createDfa(regExps[1])
printDfaStates(dfa)
