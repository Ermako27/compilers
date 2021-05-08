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
    state3.fromMoves['b'].append(state2)
    state3.fromMoves['b'].append(state5)

    state4.moves = { # D
        'a': state4, # D
        'b': state5 # E
    }
    state4.fromMoves['a'].append(state3)
    state4.fromMoves['a'].append(state4)
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