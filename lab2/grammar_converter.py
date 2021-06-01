import itertools

from grammar import Grammar, Production

# er_productions - подстановки продукций
# Nonterminals: ['S', 'A']
# Terminals: ['a', 'b', 'c', 'd']
# Start: S
# Productions:
# S -> Aa | b
# A -> Ac | Sd
# ER:  [A -> Aad, A -> bd]

class GrammarConverter:
    """
    Class to delete eps-productions and left recursion in grammar
    """

    @staticmethod
    def delete_left_recursion(g: Grammar) -> Grammar:
        grammar = Grammar(g.non_terminals, g.terminals, g.productions[:], g.start_symbol)
        # grammar = GrammarConverter.delete_eps_productions(grammar)

        # print(grammar)
        non_terms = grammar.non_terminals[:]
        n = len(non_terms)
        print('\n\nnon_terms', non_terms)
        print('----------------------------')
        for i in range(n): # верхний цикл проходит по НЕТЕРМИНАЛАМ
            print('{0}: {1}'.format(i, non_terms[i]))
            for j in range(i):
                cur_productions = []
                for p in grammar.productions:
                    print('production: ', p)
                    if p.left == non_terms[i] and p.right[0] == non_terms[j] and len(p.right) > 1:  # Ai -> Aj a
                        er_productions = grammar.er_productions(p)
                        cur_productions.extend(er_productions[:])
                    else:
                        cur_productions.append(p)
                    print('cur_productions', cur_productions)
                grammar.update_productions(cur_productions)

            grammar.delete_directly_left_recursion(non_terms[i])
            print('~~~~~~~~~~~~~~~~~~~~\n')

        return grammar
    
    @staticmethod
    def make_chomsky_form(g: Grammar) -> Grammar:
        grammar = Grammar(g.non_terminals, g.terminals, g.productions[:], g.start_symbol)
        print('\n')
        # new_productions = []

        # for p in grammar.productions:
        #     processed_productions = grammar.process_production(p)
        #     new_productions += processed_productions
        # grammar.update_productions(new_productions)
        grammar.remove_start_symbol_from_right()
        grammar.process_production()
        print(grammar)

        # for p in grammar.productions:
        #     print(p.right[0])
