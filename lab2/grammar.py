from collections import defaultdict


class Production:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} -> {''.join(self.right)}"


class Grammar:
    """
    Class describing grammar
    """
    EPS = "EPS"

    def __init__(self, non_terminals: list, terminals: list, productions: list, start_symbol: str):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def er_productions(self, production):
        left = production.left
        right = production.right
        first_right = right.pop(0)
        new_productions = []

        for p in self.productions:
            if p.left == first_right:
                new_productions.append(Production(left, p.right + right))

        # print("ER: ", new_productions)
        return new_productions

    def delete_directly_left_recursion(self, left):
        # print('\n~~~~~~~~~~~~~~~~~~~~')
        # print('delete_directly_left_recursion')
        # print('~~~~~~~~~~~~~~~~~~~~')
        # print('left: {0}'.format(left))
        # print('self.productions: {0}'.format(self.productions))
        for p in self.productions:
            if p.left == left and p.right[0] == left:
                break
        else:
            return  # no left recursion

        new_productions = []
        new_left = left + "'"
        self.non_terminals.append(new_left)

        eps_in_productions = False
        for p in self.productions:
            # print('\ncur production {0}'.format(p))
            if p.left == left:
                if p.right[0] == left:
                    new_productions.append(Production(new_left, p.right[1:] + [new_left]))
                    if not eps_in_productions:
                        new_productions.append(Production(new_left, self.EPS))
                        eps_in_productions = True

                    # new_productions.append(Production(new_left, p.right[1:]))
                    # print('new_productions {0}'.format(new_productions))
                else:
                    new_productions.append(Production(left, p.right[:] + [new_left]))
                    # new_productions.append(Production(left, p.right[:]))
                    # print('new_productions {0}'.format(new_productions))
            else:
                new_productions.append(p)
                # print('new_productions {0}'.format(new_productions))

        self.update_productions(new_productions)
    

    def process_production(self):
        new_productions = []
        
        for production in self.productions:

            if len(production.right) == 1:
                if production.right[0] in self.terminals or production.left == self.start_symbol:
                    new_productions.append(production)

            else:
                tmp_productions = self.replace_terminal_with_nonterminal(production)
                for p in tmp_productions:
                    if len(p.right) > 2:
                        new_productions += self.process_long_productions(p)
                    else:
                        new_productions.append(p)
        self.update_productions(new_productions)
    
    def remove_start_symbol_from_right(self):
        tmp_new_productions = []
        new_productions = []
        new_start_symbol = None
        prev_start_symbol = self.start_symbol
        for production in self.productions:
            # если где-то в правой части есть стартовый нетерминал, то создаем новую продукцию S' -> S
            if self.start_symbol in production.right and new_start_symbol == None:
                new_start_symbol = self.start_symbol + "'"
                tmp_new_productions.append(Production(new_start_symbol, [self.start_symbol]))
                tmp_new_productions.append(production)
                self.start_symbol = new_start_symbol
                self.non_terminals.append(new_start_symbol)
            else:
                tmp_new_productions.append(production)
        
        # если была e-продукция из стартового нетерминала, то нужно сделать новую продукцию из нового стартового нетерминала в е
        if new_start_symbol != None:
            for production in tmp_new_productions:
                if production.left == prev_start_symbol and \
                len(production.right) == 1 and \
                production.right[0] == self.EPS: # у брать старую продукцию виду S -> EPS заменив ее на S' -> EPS
                    tmp_new_productions.append(Production(new_start_symbol, [self.EPS]))
                else:
                    new_productions.append(production)

        self.update_productions(new_productions)
        

    def process_long_productions(self, production):
        right_part = production.right
        left_part = production.left

        new_productions = []

        first_non_terminal = right_part[0]
        new_non_terminal = right_part[1:]

        while len(new_non_terminal) != 1:
            formatted_new_nt = '<' + ''.join([str(nt) for nt in new_non_terminal]) + '>'
            self.non_terminals.append(formatted_new_nt)
            new_productions.append(Production(left_part, [first_non_terminal, formatted_new_nt]))

            left_part = formatted_new_nt
            first_non_terminal = new_non_terminal[0]
            new_non_terminal = new_non_terminal[1:]
        
        new_productions.append(Production(left_part, [first_non_terminal, new_non_terminal[0]]))

        return new_productions


    def replace_terminal_with_nonterminal(self, production):
        left_part = production.left
        right_part = production.right
        new_productions = []
        new_right_part = []
        for el in right_part:
            if el in self.terminals:
                left = el + "'" # создаем новый нетерминал
                additional_production = Production(left, el) # a' -> a создаем правило вывода для нового нетерминала

                if not self.is_element_in_list(left, self.non_terminals): 
                    self.non_terminals.append(left) # добавляем новый нетерминал
                
                # добавляем правила вида a' -> a, чтобы из нового нетерминала выводился старый терминал
                if not self.is_production_in_productions(additional_production, new_productions):
                    new_productions.append(additional_production)

                new_right_part.append(left) # добавляем новый нетерминал на вместо терминала

            elif el in self.non_terminals:
                new_right_part.append(el)
        result_production = Production(left_part, new_right_part)
        new_productions.append(result_production)
        return new_productions
                    




    def update_productions(self, new_productions):
        self.productions.clear()
        self.productions.extend(new_productions[:])        

    def is_production_in_productions(self, production, productions):
        for p in productions:
            if production.left == p.left and production.right == p.right:
                return True
        return False

    def is_element_in_list(self, element, list):
        for el in list:
            if el == element:
                return True
        return False

    def add_production(self, left, right):
        self.productions.append(Production(left, right))

    # def delete_eps_productions(self):
    #     for production in self.productions:
    #         if len(production.right) == 1 and production.right[0] == self.EPS:
    #             self.productions.remove(production)

    def _repr_productions(self):
        productions = defaultdict(list)
        for production in self.productions:
            productions[production.left].append("".join(production.right))

        repr_string = ""
        for left, rights in productions.items():
            repr_string += f"\n{left} -> {' | '.join(rights)}"

        return repr_string

    def __repr__(self):
        return "Nonterminals: {0}\nTerminals: {1}\nStart: {2}\nProductions:{3}".format(self.non_terminals,
                                                                                       self.terminals,
                                                                                       self.start_symbol,
                                                                                       self._repr_productions())
