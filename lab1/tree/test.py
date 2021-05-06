from graphviz import Digraph
from tree import createPolishNotation, createTree
from dfa import createDfa, createTestDfa, minimizeDfa

regExps = ['(a|b)*abb', 'a*b*(aa*|b)']

def createTreeEdges(root, graph):
    if root.left != None:
        graph.edge(root.nodeId, root.left.nodeId)
        createTreeEdges(root.left, graph)

    if root.right != None:
        graph.edge(root.nodeId, root.right.nodeId)
        createTreeEdges(root.right, graph)

def renderTree(root):
    astGraph = Digraph('AST', filename='astGraph.gv')

    createTreeEdges(root, astGraph)

    astGraph.render()

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
        print(state.positions, ' | ', state.stateId)

def renderDfa(dfa, filename):
    file = '{0}.gv'.format(filename)
    dfaGraph = Digraph('DFA', filename=file)
    dfaGraph.attr(rankdir='LR', size='8,5')
    dfaGraph.attr('node', shape='doublecircle')
    for state in dfa.states:
        if state.isFinalState:
            dfaGraph.node(', '.join([str(pos) for pos in state.positions]))

    dfaGraph.attr('node', shape='circle')
    for state in dfa.states: 
        edge1 = ', '.join([str(pos) for pos in state.positions])
        if state.isStartState:
            dfaGraph.node('s', shape='point')
            dfaGraph.edge('s', edge1)
        for symbol, nextState in state.moves.items():
            edge2 = ', '.join([str(pos) for pos in nextState.positions])
            dfaGraph.edge(edge1, edge2, label=symbol)

    dfaGraph.render()

def printMinimizedClasses(classes):
    print('\n\n\nMinimazed states')
    print('----------------------')
    num = 1
    for eqvClassId, eqvClass in classes.items():
        print('class {0}'.format(num))
        for state in eqvClass:
            print('    state: ', state.positions)
        num += 1


########## TREE TEST ##########
tree = createTree(regExps[1])
printFollowPos(tree)
printNumed(tree)
renderTree(tree.root)

########## DFA TEST ##########
dfa1 = createDfa(regExps[1])
printDfaStates(dfa1)
renderDfa(dfa1, 'dfaGraph')

dfa2 = createTestDfa()
printDfaStates(dfa2)
renderDfa(dfa2, 'testDfa')
minimizedClasses,  minimizeDfa2 = minimizeDfa(dfa2)
printMinimizedClasses(minimizedClasses)
renderDfa(minimizeDfa2, 'minimizedTestDfa')