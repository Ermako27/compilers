from graphviz import Digraph
from tree import createPolishNotation, createTree
from dfa import createDfa

regExps = ['(a|b)*abb', 'a*b*(aa*|b)']

astGraph = Digraph('AST', filename='astGraph.gv');
dfaGraph = Digraph('DFA', filename='dfaGraph.gv');
dfaGraph.attr(rankdir='LR', size='8,5')

def createTreeEdges(root):
    print(root.nodeId,' firstPos:',root.firstPos)
    print(root.nodeId,' lastPos:',root.lastPos)
    print(root.nodeId,' nullable:',root.nullable)
    print('-------------------------------------')

    if root.left != None:
        astGraph.edge(root.nodeId, root.left.nodeId)
        createTreeEdges(root.left)

    if root.right != None:
        astGraph.edge(root.nodeId, root.right.nodeId)
        createTreeEdges(root.right)

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

def createDfaEdges(dfa):
    dfaGraph.attr('node', shape='doublecircle')
    for state in dfa.states:
        if state.isFinalState:
            dfaGraph.node(', '.join([str(pos) for pos in state.positions]))

    dfaGraph.attr('node', shape='circle')
    for state in dfa.states: 
        edge1 = ', '.join([str(pos) for pos in state.positions])
        for symbol, nextState in state.moves.items():
            edge2 = ', '.join([str(pos) for pos in nextState.positions])
            dfaGraph.edge(edge1, edge2, label=symbol) 


tree = createTree(regExps[0])
createTreeEdges(tree.root)
printFollowPos(tree)
printNumed(tree)
astGraph.render()

dfa = createDfa(regExps[0])
createDfaEdges(dfa)
printDfaStates(dfa)
dfaGraph.render()
