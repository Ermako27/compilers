from tree import createTree

class State():
    def __init__(self):
        self.positions = set()
        # self.stateId = "".join([str(pos) for pos in positions])
        self.moves = {} # словарь вида {'a': [State, State]}
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
            if dfa.isAlreadyHave(state): # если такое состояние у нас уже есть
                alreadyHaveState = dfa.getStateByPositions(state.positions) # то берем состоние, которое у нас уже есть
                currentState.moves[moveSymbol] = alreadyHaveState # и присваевам его в каче-ве перехода 
            else:
                currentState.moves[moveSymbol] = state # присваиваем свежесозданное состояние
                dfa.states.append(state) # добавляем в список состояний автомата

        currentState.isVisited = True
    
    return dfa
    

    

