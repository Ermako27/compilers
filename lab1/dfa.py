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
        self.combinedTo = None # если это состояние было соединено в какое-то новое при минимизации, то здесь будет ссылка на новосформированное состояние

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

    def getStartState(self):
        for state in self.states:
            if state.isStartState:
                return state
        return None
        


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

def isStateInClasses(eqvClasses, state):
    for eqvClassId, eqvClass in eqvClasses.items():
        if isStateInClass(eqvClass, state):
            return True
    return False

def createNewDfaStates(equivalenceClasses, dfa):
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
                state.combinedTo = newState # ссылка на состояние, которое было получено путем соединения этого с еще какими-то состояниями
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
                        # если следующее состояние было скомбинировано в какое-то новое
                        if nextState.combinedTo != None:
                            newState.moves[symbol] = nextState.combinedTo # ставим новому состоянию переход в следующее
                            # добавляем вместо них в fromMoves новое соединенное состояние
                            nextState.combinedTo.fromMoves[symbol].append(newState)
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

    return newStates

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

def printClassStates(eqvClass, name =''):
    print(name)
    for state in eqvClass:
        print(state.positions)

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

    classSymbolPairQueue = []

    # заполняем очередь состояний
    for symbol in dfa.alphabet:
        classSymbolPairQueue.append(tuple([nonFinalStates, symbol])) # пара <C, a> , где С - класс состояний, a - символ по которому делается переход (ребро)
        classSymbolPairQueue.append(tuple([finalStates, symbol]))

    while len(classSymbolPairQueue) != 0:
        classSymbolPair = classSymbolPairQueue.pop(0)

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
                    pair = tuple([eqvClass, symbol])
                    if isClassSymbolPairInQueue(classSymbolPairQueue, pair):
                        classSymbolPairQueue = removeClassSymbolPairFromQueue(classSymbolPairQueue, pair)
                        classSymbolPairQueue.append(tuple([newClass1, symbol]))
                        classSymbolPairQueue.append(tuple([newClass2, symbol]))
                    else:
                        if len(newClass1) <= len(newClass2):
                            classSymbolPairQueue.append(tuple([newClass1, symbol]))
                        else:
                            classSymbolPairQueue.append(tuple([newClass2, symbol])) 
        equivalenceClasses = tmpEquivalenceClasses.copy()

    dfa.states = createNewDfaStates(equivalenceClasses.copy(), dfa)

    return equivalenceClasses, dfa

def checkMatch(regExp, exp):
    dfa = createDfa(regExp)
    eqvClasses, minimizedDfa = minimizeDfa(dfa)

    currentState = minimizedDfa.getStartState()
    if len(exp) == 0:
        if currentState.isFinalState:
            return True
        else:
            return False

    for word in exp:
        if word not in currentState.moves:
            return False
        currentState = currentState.moves[word]
    return currentState.isFinalState



def isEqualClasses(eqvClass1, eqvClass2):
    if len(eqvClass1) != len(eqvClass2):
        return False
    for state in eqvClass1:
        if not isStateInClass(eqvClass2, state):
            return False
    return True
def isEqualClassSymbolPair(pair1, pair2):
    if isEqualClasses(pair1[0], pair2[0]) and pair1[1] == pair2[1]:
        return True
    return False
def isClassSymbolPairInQueue(queue, pairToFind):
    # pairToFind[0] - класс эквиваленции
    # pairToFind[1] - символ, по которому осуществляется переход
    for pair in queue:
        if isEqualClasses(pair[0], pairToFind[0]) and pair[1] == pairToFind[1]:
            return True
    return False
def removeClassSymbolPairFromQueue(queue, pairToRemove):
    newQueue = []
    for pair in queue:
        if not isEqualClassSymbolPair(pair, pairToRemove):
            newQueue.append(pair)
    return newQueue
def printClassStates(eqvClass, name =''):
    print(name)
    for state in eqvClass:
        print(state.positions)
def printClasses(classes):
    for i, eqvClass in classes.items():
        printClassStates(eqvClass)



# реализовать лексер intlr
# синтаксический анализатор

# этапы курсача:
# 1) лексер