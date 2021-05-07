from graphviz import Digraph
from tree import createPolishNotation, createTree
from dfa import createDfa, minimizeDfa, State, Dfa, checkMatch

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
        print('state moves:')
        for symbol, nextState in state.moves.items():
            print('    {0}: {1}'.format(symbol, nextState.positions))
        print('state from moves:')
        for symbol, prevStates in state.fromMoves.items():
            for prevState in prevStates:
                print('    {0}: {1}'.format(symbol, prevState.positions))
        print()
    
    print('Dfa alphabet: ', dfa.alphabet)

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


def createTestDfa1():
    # https://www.youtube.com/watch?v=0XaGAkY09Wc
    dfa = Dfa(set(['a', 'b']))
    # создаем состаяния
    state1 = State(dfa.alphabet) # A
    state1.positions = set([1])
    state1.stateId = '1'
    state1.isStartState = True

    state2 = State(dfa.alphabet) # B
    state2.positions = set([2])
    state2.stateId = '2'

    state3 = State(dfa.alphabet) # C
    state3.positions = set([3])
    state3.stateId = '3'

    state4 = State(dfa.alphabet) # D
    state4.positions = set([4])
    state4.stateId = '4'

    state5 = State(dfa.alphabet) # E
    state5.positions = set([5])
    state5.stateId = '5'
    state5.isFinalState = True

    # выставляем переходы
    state1.moves = {
        'a': state2,
        'b': state3
    }

    state2.moves = {
        'a': state2,
        'b': state4
    }

    state3.moves = {
        'a': state2,
        'b': state3
    }

    state4.moves = {
        'a': state2,
        'b': state5
    }

    state5.moves = {
        'a': state2,
        'b': state3
    }

    dfa.states = [state1, state2, state3, state4, state5]

    return dfa

def createTestDfa2():
    # https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%91%D1%80%D0%B6%D0%BE%D0%B7%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE
    # создаем состаяния
    dfa = Dfa(set(['a', 'b']))
    state0 = State(dfa.alphabet)
    state0.positions = set([0])
    state0.stateId = '0'
    state0.isStartState = True

    state1 = State(dfa.alphabet)
    state1.positions = set([1])
    state1.stateId = '1'

    state2 = State(dfa.alphabet)
    state2.positions = set([2])
    state2.stateId = '2'
    state2.isFinalState = True

    state3 = State(dfa.alphabet)
    state3.positions = set([3])
    state3.stateId = '3'
    state3.isFinalState = True

    # выставляем переходы
    state0.moves = {
        'b': state1
    }

    state1.moves = {
        'a': state2,
        'b': state3
    }

    state2.moves = {
        'a': state2,
        'b': state3
    }

    dfa.states = [state0, state1, state2, state3]

    return dfa

def createTestDfa3():
    # https://neerc.ifmo.ru/wiki/index.php?title=%D0%9C%D0%B8%D0%BD%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D0%94%D0%9A%D0%90,_%D0%B0%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%B7%D0%B0_O(n%5E2)_%D1%81_%D0%BF%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BD%D0%B8%D0%B5%D0%BC_%D0%BF%D0%B0%D1%80_%D1%80%D0%B0%D0%B7%D0%BB%D0%B8%D1%87%D0%B8%D0%BC%D1%8B%D1%85_%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B9
    # создаем состаяния
    dfa = Dfa(set(['a', 'b']))
    state1 = State(dfa.alphabet) # A
    state1.positions = set([1])
    state1.stateId = '1'
    state1.isStartState = True

    state2 = State(dfa.alphabet) # B
    state2.positions = set([2])
    state2.stateId = '2'

    state3 = State(dfa.alphabet) # C
    state3.positions = set([3])
    state3.stateId = '3'

    state4 = State(dfa.alphabet) # D
    state4.positions = set([4])
    state4.stateId = '4'

    state5 = State(dfa.alphabet) # E
    state5.positions = set([5])
    state5.stateId = '5'

    state6 = State(dfa.alphabet) # F
    state6.positions = set([6])
    state6.stateId = '6'
    state6.isFinalState = True

    state7 = State(dfa.alphabet) # G
    state7.positions = set([7])
    state7.stateId = '7'
    state7.isFinalState = True

    state8 = State(dfa.alphabet) # H
    state8.positions = set([8])
    state8.stateId = '8'

    state1.moves = { # A
        'a': state8, # H
        'b': state2 # B
    }

    state2.moves = { # B
        'a': state8, # H
        'b': state1 # A
    }
    state2.fromMoves['b'].append(state1)

    state3.moves = { # C
        'a': state5, # E
        'b': state6 # F
    }
    state3.fromMoves['a'].append(state8)
    state3.fromMoves['b'].append(state8)

    state4.moves = { # D
        'a': state5, # E
        'b': state6 # F
    }

    state5.moves = { # E
        'a': state6, # F
        'b': state7 # G
    }
    state5.fromMoves['a'].append(state3)
    state5.fromMoves['a'].append(state4)


    state6.moves = { # F
        'a': state6, # F
        'b': state6 # F
    }
    state6.fromMoves['a'].append(state5)
    state6.fromMoves['a'].append(state6)
    state6.fromMoves['b'].append(state3)
    state6.fromMoves['b'].append(state7)
    state6.fromMoves['b'].append(state4)
    state6.fromMoves['b'].append(state6)

    state7.moves = { # G
        'a': state7, # G
        'b': state6 # F
    }
    state7.fromMoves['a'].append(state7)
    state7.fromMoves['b'].append(state5)

    state8.moves = { # H
        'a': state3, # C
        'b': state3 # C
    }
    state8.fromMoves['a'].append(state1)
    state8.fromMoves['a'].append(state2)



    # выставляем переходы

    dfa.states = [state1, state2, state3, state4, state5, state6, state7, state8]

    return dfa

def createTestDfa4():
    # из буниной
    # создаем состаяния
    dfa = Dfa(set(['a', 'b']))
    state1 = State(dfa.alphabet) # A
    state1.positions = set([1])
    state1.stateId = '1'
    state1.isStartState = True

    state2 = State(dfa.alphabet) # B
    state2.positions = set([2])
    state2.stateId = '2'

    state3 = State(dfa.alphabet) # C
    state3.positions = set([3])
    state3.stateId = '3'
    state3.isFinalState = True

    state4 = State(dfa.alphabet) # D
    state4.positions = set([4])
    state4.stateId = '4'

    state5 = State(dfa.alphabet) # E
    state5.positions = set([5])
    state5.stateId = '5'
    state5.isFinalState = True

    state1.moves = { # A
        'a': state2, # B
        'b': state4 # D
    }

    state2.moves = { # B
        'a': state2, # B
        'b': state3 # C
    }
    state2.fromMoves['a'].append(state1)
    state2.fromMoves['a'].append(state2)
    state2.fromMoves['a'].append(state5)

    state3.moves = { # C
        'a': state4, # D
        'b': state5 # E
    }
    state3.fromMoves['b'].append(state3)
    state3.fromMoves['b'].append(state5)

    state4.moves = { # D
        'a': state4, # D
        'b': state5 # E
    }
    state4.fromMoves['a'].append(state3)
    state4.fromMoves['b'].append(state1)

    state5.moves = { # E
        'a': state2, # B
        'b': state3 # C
    }
    state5.fromMoves['b'].append(state3)
    state5.fromMoves['b'].append(state4)

    # выставляем переходы

    dfa.states = [state1, state2, state3, state4, state5]

    return dfa

def createTestDfa5():
    # http://trpl.narod.ru/Conspectus/trpl_2012_05.htm
    # создаем состаяния
    dfa = Dfa(set(['a', 'b']))
    state1 = State(dfa.alphabet) # A
    state1.positions = set([1])
    state1.stateId = '1'
    state1.isStartState = True
    state1.isFinalState = True

    state2 = State(dfa.alphabet) # B
    state2.positions = set([2])
    state2.stateId = '2'

    state3 = State(dfa.alphabet) # C
    state3.positions = set([3])
    state3.stateId = '3'
    state3.isFinalState = True

    state4 = State(dfa.alphabet) # D
    state4.positions = set([4])
    state4.stateId = '4'
    state4.isFinalState = True

    state5 = State(dfa.alphabet) # E
    state5.positions = set([5])
    state5.stateId = '5'

    state1.moves = { # A
        'a': state2, # B
        'b': state3 # C
    }

    state2.moves = { # B
        'a': state4, # D
        'b': state5 # E
    }
    state2.fromMoves['a'].append(state1)
    state2.fromMoves['a'].append(state3)
    state2.fromMoves['a'].append(state4)

    state3.moves = { # C
        'a': state2, # B
        'b': state3 # C
    }
    state3.fromMoves['b'].append(state1)
    state3.fromMoves['b'].append(state4)
    state3.fromMoves['b'].append(state3)

    state4.moves = { # D
        'a': state2, # B
        'b': state3 # C
    }
    state4.fromMoves['a'].append(state2)
    state4.fromMoves['a'].append(state5)

    state5.moves = { # E
        'a': state4, # D
        'b': state5 # E
    }
    state5.fromMoves['b'].append(state2)
    state5.fromMoves['b'].append(state5)

    # выставляем переходы

    dfa.states = [state1, state2, state3, state4, state5]

    return dfa

########## TREE TEST ##########
tree = createTree(regExps[1])
printFollowPos(tree)
printNumed(tree)
renderTree(tree.root)

########## DFA TEST ##########
dfa1 = createDfa(regExps[1])
printDfaStates(dfa1)
renderDfa(dfa1, 'dfaGraph')
minimizeRegExpClasses,  minimizeRegExpDfa = minimizeDfa(dfa1)
printMinimizedClasses(minimizeRegExpClasses)
renderDfa(minimizeRegExpDfa, 'minimizeRegExpDfa')

########## REG EXP TEST ##########
print('check match a | a: ', checkMatch('a', 'a'))
print('check match a | aa: ', checkMatch('a', 'aa'))
print('check match a | empty: ', checkMatch('a', ''))
print('check match ab | ab: ', checkMatch('ab', 'ab'))

########## DFA MINIMIZATION TEST ##########
# # 1
# testDfa1 = createTestDfa1()
# printDfaStates(testDfa1)
# renderDfa(testDfa1, 'testDfa1')
# minimizedClasses1,  minimizeTestDfa1 = minimizeDfa(testDfa1)
# printMinimizedClasses(minimizedClasses1)
# renderDfa(minimizeTestDfa1, 'minimizeTestDfa1')

# # 2
# testDfa2 = createTestDfa2()
# printDfaStates(testDfa2)
# renderDfa(testDfa2, 'testDfa2')
# minimizedClasses2,  minimizeTestDfa2 = minimizeDfa(testDfa2)
# printMinimizedClasses(minimizedClasses2)
# renderDfa(minimizeTestDfa2, 'minimizeTestDfa2')

# # 3
# testDfa3 = createTestDfa3()
# printDfaStates(testDfa3)
# renderDfa(testDfa3, 'testDfa3')
# minimizedClasses3,  minimizeTestDfa3 = minimizeDfa(testDfa3)
# printMinimizedClasses(minimizedClasses3)
# renderDfa(minimizeTestDfa3, 'minimizeTestDfa3')

# # 4
# testDfa4 = createTestDfa4()
# printDfaStates(testDfa4)
# renderDfa(testDfa4, 'testDfa4')
# minimizedClasses4,  minimizeTestDfa4 = minimizeDfa(testDfa4)
# printMinimizedClasses(minimizedClasses4)
# renderDfa(minimizeTestDfa4, 'minimizeTestDfa4')

# #5
# testDfa5 = createTestDfa5()
# printDfaStates(testDfa5)
# renderDfa(testDfa5, 'testDfa5')
# minimizedClasses5,  minimizeTestDfa5 = minimizeDfa(testDfa5)
# printMinimizedClasses(minimizedClasses5)
# renderDfa(minimizeTestDfa5, 'minimizeTestDfa5')