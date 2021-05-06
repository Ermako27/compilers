from tree import createTree

class State():
    def __init__(self):
        self.positions = set()
        self.moves = {} # словарь вида {'a': [State, State]}
        self.stateId = ''
        self.isStartState = False
        self.isFinalState = False
        self.isVisited = False

class Dfa():
    def __init__(self):
        self.states = []

    def getFirstUnvisitedState(self):
        for state in self.states:
            if not state.isVisited:
                return state
        return None

    def getStateByPositions(self,positions):
        for state in self.states:
            if state.positions == positions:
                return state
        return None

    def isAlreadyHave(self, newState):
        for state in self.states:
            if state.positions == newState.positions:
                return True
        return False
    
    def isAllStateVisited(self):
        for state in self.states:
            if not state.isVisited:
                return False
        return True
        


def createDfa(regExp):
    dfa = Dfa()

    tree = createTree(regExp)
    firstPos = tree.root.firstPos

    startState = State()
    startState.positions = firstPos
    startState.isStartState = True

    dfa.states.append(startState)

    currentState = startState

    while not dfa.isAllStateVisited():
        currentState = dfa.getFirstUnvisitedState()
        tmpMoves = {} # временная мапа, хранящаяя переходы в новые состояния

        # для каждой позиции в текущем состоянии
        for pos in currentState.positions:
            symbol = tree.numed[pos] # смотрим какая буква соответствует позиции
            if symbol != '#':
                if symbol not in tmpMoves: # если во временной мапе еще нет перехода по такой букве
                    tmpMoves[symbol] = State() # то создаем переход в новое состояние

                # тут по коду ясно
                tmpMoves[symbol].positions = tmpMoves[symbol].positions.union(tree.followPos[str(pos)])
            else: # если в состоянии оказалась позиция решетки, то это финальное состояние
                currentState.isFinalState = True

        # решаем что делать с переходами во временной мапе
        for moveSymbol, state in tmpMoves.items():
            state.stateId = ''.join([str(pos) for pos in state.positions])
            if dfa.isAlreadyHave(state): # если такое состояние у нас уже есть
                alreadyHaveState = dfa.getStateByPositions(state.positions) # то берем состоние, которое у нас уже есть
                currentState.moves[moveSymbol] = alreadyHaveState # и присваевам его в каче-ве перехода 
            else:
                currentState.moves[moveSymbol] = state # присваиваем свежесозданное состояние
                dfa.states.append(state) # добавляем в список состояний автомата

        currentState.isVisited = True
    
    return dfa

def createTestDfa():
    # создаем состаяния
    state1 = State() # A
    state1.positions = set([1])
    state1.isStartState = True

    state2 = State() # B
    state2.positions = set([2])

    state3 = State() # C
    state3.positions = set([3])

    state4 = State() # D
    state4.positions = set([4])

    state5 = State() # E
    state5.positions = set([5])
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

    dfa = Dfa()
    dfa.states = [state1, state2, state3, state4, state5]

    return dfa


def minimizeDfa():
    dfa = createTestDfa()

    # создали классы 0-эквивалентности
    nonFinalStates = set()
    finalStates = set()
    for state in dfa.states:
        if state.isFinalState:
            finaleStates.add(state)
        else:
            nonFinaleStates.add(state)

    # список всех классов разбиения, изпользуем словарь, чтобы можно было легко попнуть по id
    # здесь id - конкатенация stateId всех состояний в классе
    equivalenceClasses = {
        ''.join([state.stateId for state in nonFinalStates]): nonFinalStates
        ''.join([state.stateId for state in finalStates]): finalStates
    }
    stateQueue = []

    # заполняем очередь состояний
    for state in nonFinalStates:
        stateQueue.append(state)
    for state in finalStates:
        stateQueue.append(state)
    
    while len(stateQueue) != 0:
        state = stateQueue.pop(0)

        for eqvClassId, eqvClass in equivalenceClasses.items():
            # должно возвращать два set(), например eqvClass = {A,B,C,D}; newClass1 = {A,B,C}, newClass2 = {D}
            # где каждая A,B,C,D есть state
            newClass1, newClass2 = splitClass(eqvClass, state)

            if (newClass1 != None and newClass2 != None):
                equivalenceClasses.pop(eqvClassId)

                newClass1Id = ''.join([state.stateId for state in newClass1])
                equivalenceClasses[newClass1Id] = newClass1

                newClass2Id = ''.join([state.stateId for state in newClass2])
                equivalenceClasses[newClass2Id] = newClass2

                # добавляем в очередь состояний, состояния из новых классов
                for state in newClass1:
                    stateQueue.append(state)

                for state in newClass2:
                    stateQueue.append(state)

    return equivalenceClasses




def splitClass(eqvClass, state):
    pass