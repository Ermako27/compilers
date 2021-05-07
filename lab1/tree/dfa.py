from tree import createTree

class State():
    def __init__(self, alphabet):
        self.positions = set()
        self.moves = {} # словарь вида {'a': [State, State]}, куда мы можем перейти из этого состояния
        self.fromMoves = {symbol:[] for symbol in alphabet} # словарь вида {'a': [State, State]}, откуда мы можем перейти в это состояние
        self.stateId = ''
        self.isStartState = False
        self.isFinalState = False
        self.isVisited = False

class Dfa():
    def __init__(self, alphabet):
        self.states = []
        self.alphabet = alphabet

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
    tree = createTree(regExp)
    dfa = Dfa(tree.alphabet)
    
    firstPos = tree.root.firstPos

    startState = State(dfa.alphabet)
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
                    tmpMoves[symbol] = State(dfa.alphabet) # то создаем переход в новое состояние

                # тут по коду ясно
                tmpMoves[symbol].positions = tmpMoves[symbol].positions.union(tree.followPos[str(pos)])
            else: # если в состоянии оказалась позиция решетки, то это финальное состояние
                currentState.isFinalState = True

        # решаем что делать с переходами во временной мапе
        for moveSymbol, state in tmpMoves.items():
            if dfa.isAlreadyHave(state): # если такое состояние у нас уже есть
                alreadyHaveState = dfa.getStateByPositions(state.positions) # то берем состоние, которое у нас уже есть
                currentState.moves[moveSymbol] = alreadyHaveState # и присваевам его в каче-ве перехода

                alreadyHaveState.fromMoves[moveSymbol].append(currentState) # сохраняем ссылку на предыдущее состояние
            else:
                currentState.moves[moveSymbol] = state # присваиваем свежесозданное состояние

                state.fromMoves[moveSymbol].append(currentState) # сохраняем ссылку на предыдущее состояние

                dfa.states.append(state) # добавляем в список состояний автомата

        currentState.isVisited = True

    for state in dfa.states:
        state.stateId = ''.join([str(pos) for pos in state.positions])
    
    return dfa

def isStateInClass(eqvClass, stateToFind):
    for state in eqvClass:
        if state.stateId == stateToFind.stateId:
            return True
    return False

def splitClass(eqvClass, classSymbolPair):
    newClass1 = None
    newClass2 = None

    spliterClass = classSymbolPair[0]
    symbol = classSymbolPair[1]

    for state in eqvClass:
        if symbol in state.moves and isStateInClass(spliterClass, state.moves[symbol]):
            if newClass1 == None:
                newClass1 = set()
            newClass1.add(state)
        else:
            if newClass2 == None:
                newClass2 = set()
            newClass2.add(state)

    return newClass1, newClass2

def minimizeDfa(dfa):
    # создали классы 0-эквивалентности
    nonFinalStates = set()
    finalStates = set()
    for state in dfa.states:
        if state.isFinalState:
            finalStates.add(state)
        else:
            nonFinalStates.add(state)

    # классы разбиения, изпользуем словарь, чтобы можно было легко попнуть по id
    equivalenceClasses = {
        '1': nonFinalStates,
        '2': finalStates
    }
    # используем далее эту переменную в качестве id для новых классов
    lastClassId = len(equivalenceClasses)

    stateQueue = []

    # заполняем очередь состояний
    for symbol in dfa.alphabet:
        stateQueue.append(tuple([nonFinalStates, symbol])) # пара <C, a> , где С - класс состояний, a - символ по которому делается переход (ребро)
        stateQueue.append(tuple([finalStates, symbol]))

    while len(stateQueue) != 0:
        classSymbolPair = stateQueue.pop(0)

        tmpEquivalenceClasses = equivalenceClasses.copy()
        for eqvClassId, eqvClass in equivalenceClasses.items():
            # должно возвращать два set(), например eqvClass = {A,B,C,D}; newClass1 = {A,B,C}, newClass2 = {D}
            # где каждая A,B,C,D есть state
            newClass1, newClass2 = splitClass(eqvClass, classSymbolPair)

            if newClass1 != None and newClass2 != None:
                tmpEquivalenceClasses.pop(eqvClassId)

                lastClassId += 1
                tmpEquivalenceClasses[str(lastClassId)] = newClass1
                lastClassId += 1
                tmpEquivalenceClasses[str(lastClassId)] = newClass2

                for symbol in dfa.alphabet:
                    stateQueue.append(tuple([newClass1, symbol]))
                    stateQueue.append(tuple([newClass2, symbol]))
        equivalenceClasses = tmpEquivalenceClasses.copy()

    # создаем список состояний составленных из эквивалентных
    newStates = []
    for eqvClassId, eqvClass in equivalenceClasses.items():
        if (len(eqvClass) == 1):
            state = eqvClass.pop()
            newStates.append(state)
        else:
            newState = State(dfa.alphabet)
            for state in eqvClass:
                newState.positions = newState.positions.union(state.positions)
                newState.isStartState = newState.isStartState or state.isStartState
                newState.isFinalState = newState.isFinalState or state.isFinalState
            newState.stateId = ''.join([str(pos) for pos in newState.positions])

            # для каждого состояния из класса эквиваленции
            for state in eqvClass:
                # данный цикл нужен чтобы соединить состояния, В которые раньше шли состояния из класса эквиваленции, с новым состоянием
                # которое как раз и состоит из состояний из класса эквиваленции
                for symbol, nextState in state.moves.items():
                    # если следующее состояние есть в текущем классе эквиваленции
                    if isStateInClass(eqvClass, nextState):
                        newState.moves[symbol] = newState # значит делаем переход из нового состояния в себя же
                        newState.fromMoves[symbol].append(newState)
                    else:
                        newState.moves[symbol] = nextState # ставим новому состоянию переход в следующее
                        # добавляем вместо них в fromMoves новое соединенное состояние
                        nextState.fromMoves[symbol].append(newState)

                # данный цикл нужен чтобы соединить состояния, которые раньше шли В состояния из класса эквиваленции, с новым состоянием
                # которое как раз и состоит из состояний из класса эквиваленции
                for symbol, prevStates in state.fromMoves.items():
                    for prevState in prevStates:
                        prevState.moves[symbol] = newState
                        newState.fromMoves[symbol].append(prevState)

            newStates.append(newState)

    dfa.states = newStates

    return equivalenceClasses, dfa

def isStateInClasses(eqvClasses, state):
    for eqvClassId, eqvClass in eqvClasses.items():
        if isStateInClass(eqvClass, state):
            return True
    return False

#----------------------------------------------

    # # заполняем очередь состояний
    # for state in nonFinalStates:
    #     stateQueue.append(state)
    # for state in finalStates:
    #     stateQueue.append(state)
    
    # while len(stateQueue) != 0:
    #     state = stateQueue.pop(0)

    #     for eqvClassId, eqvClass in equivalenceClasses.items():
    #         # должно возвращать два set(), например eqvClass = {A,B,C,D}; newClass1 = {A,B,C}, newClass2 = {D}
    #         # где каждая A,B,C,D есть state
    #         newClass1, newClass2 = splitClass(eqvClass, state)

    #         if (newClass1 != None and newClass2 != None):
    #             equivalenceClasses.pop(eqvClassId)

                # newClass1Id = ''.join([state.stateId for state in newClass1])
                # equivalenceClasses[newClass1Id] = newClass1

                # newClass2Id = ''.join([state.stateId for state in newClass2])
                # equivalenceClasses[newClass2Id] = newClass2

    #             # добавляем в очередь состояний, состояния из новых классов
    #             for state in newClass1:
    #                 stateQueue.append(state)

    #             for state in newClass2:
    #                 stateQueue.append(state)

    # return equivalenceClasses