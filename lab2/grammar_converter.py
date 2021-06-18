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

        non_terms = grammar.non_terminals[:]
        n = len(non_terms)
        for i in range(n): # верхний цикл проходит по НЕТЕРМИНАЛАМ
            # print('{0}: {1}'.format(i, non_terms[i]))
            for j in range(i):
                cur_productions = []
                for p in grammar.productions:
                    if p.left == non_terms[i] and p.right[0] == non_terms[j] and len(p.right) > 1:  # Ai -> Aj a
                        er_productions = grammar.er_productions(p)
                        cur_productions.extend(er_productions[:])
                    else:
                        cur_productions.append(p)
                grammar.update_productions(cur_productions)

            grammar.delete_directly_left_recursion(non_terms[i])
        return grammar
    
    @staticmethod
    def make_chomsky_form(g: Grammar) -> Grammar:
        grammar = Grammar(g.non_terminals, g.terminals, g.productions[:], g.start_symbol)

        grammar.remove_start_symbol_from_right()
        grammar.process_production()

        return grammar

