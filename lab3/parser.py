from parse_tree import ParseTree

class Expression:
    def __init__(self) -> None:
        # self.productions = []
        self.logExpression = None
        self.dsc = "<выражение>"
    def addProdution(self, node):
        self.productions.append(node)


class LogExpression:
    def __init__(self) -> None:

        # self.productions = []
        self.logMon = None
        self.logExpression_ = None
        self.dsc = "<логическое выражение>"

    def addProdution(self, node):
        self.productions.append(node)

class LogExpression_:
    def __init__(self) -> None:

        # self.productions = []
        self.logOperation = None
        self.logMon = None
        self.logExpression_ = None
        self.dsc = "<логическое выражение>_"

    def addProdution(self, node):
        self.productions.append(node)

class LogMon:
    def __init__(self) -> None:

        # self.productions = []
        self.secExpression = None
        self.logMon_ = None
        self.dsc = "<логический одночлен>"

    def addProdution(self, node):
        self.productions.append(node)

class LogMon_:
    def __init__(self) -> None:

        # self.productions = []
        self.logOperation = None
        self.secExpression = None
        self.logMon_ = None
        self.dsc = "<логический одночлен>_"

    def addProdution(self, node):
        self.productions.append(node)

class SecExpr:
    def __init__(self) -> None:
        # self.productions = [
        #     [],
        #     []
        # ]
        self.firtExpression = None
        self.logOperation = None
        self.firtExpression = None
        self.dsc = "<вторичное логическое выражение>"

    def addFirstProdution(self, node):
        self.productions[0].append(node)
    
    def addSecondProdution(self, node):
        self.productions[1].append(node)

class FisrtExpr: 
    def __init__(self) -> None:
        # self.productions = [
        #     [],
        #     []
        # ]
        self.logValue = None
        self.indetificator = None
        self.dsc = "<первичное логическое выражение>"

    def addFirstProdution(self, node):
        self.productions[0].append(node)
    
    def addSecondProdution(self, node):
        self.productions[1].append(node)
    
class LogOperation:
    def __init__(self, value) -> None:
        self.value = value
        self.dsc = "<знак логической операции>"

class LogValue:
    def __init__(self) -> None:
        self.value = None
        self.dsc = "<логическое значение>"

    def addProdution(self, node):
        self.productions.append(node)



class Identifier:
    def __init__(self) -> None:
        self.value = None
        self.dsc = "<идентификатор>"

    def addProdution(self, node):
        self.productions.append(node)




class Parser:
    def __init__(self, string):
        self.string = string.replace(" ", "")
        self.identifiers = list(chr(i) for i in range(65, 91)) # 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.index = 0
        self.tree = None

    def get_tree(self):
        return self.tree

    def accept_string(self):
        tree = self._expression()
        if tree is not None and self._string_is_end():
            self.tree = tree
            return True

        return False

    def _expression(self):
        # print('_expression')

        # tree = ParseTree("Expr")

        tree = Expression()
        node = self._log_expr()
        # print('_expression() -> _log_expr(): {0}'.format(node)) # @
        # print('~~~~~~~~~~~~~~\n')
        if node is not None:
            # tree.add_child(node)
            # tree.addProdution(node)
            tree.logExpression = node

            return tree

        return None

    def _log_expr(self):
        # print('_log_expr')
        # tree = ParseTree("log expr")
        tree = LogExpression()
        log_node = self._log_mon()
        # print('_log_expr() -> _log_mon(): {0}'.format(log_node)) # @
        # print('-----------------')
        if log_node is not None:
            # tree.add_child(log_node)
            # tree.addProdution(log_node)
            tree.logMon = log_node

        log_expr_node = self._log_expr_()
        # print('_log_expr(): log_expr_node {0}'.format(log_expr_node))
        # print('~~~~~~~~~~~~~~\n')
        if log_expr_node is not None:
            # tree.add_child(log_expr_node)
            # tree.addProdution(log_expr_node)
            tree.logExpression_ = log_expr_node

        if tree.logMon or tree.logExpression_:
            return tree

        return None

    def _log_expr_(self):
        # print('_log_expr_')
        if self._out_of_range():
            return None

        # tree = ParseTree("log expr'")
        tree = LogExpression_()

        if self.string[self.index] == "!":
            self.index += 1
            # tree.add_child(ParseTree("!"))
            # tree.addProdution(LogOperation('!'))
            tree.logOperation = LogOperation('!')

            log_mon_node = self._log_mon()
            # print('log_mon_node {0}'.format(log_mon_node))
            # print('-----------------')
            if log_mon_node:
                # tree.add_child(log_mon_node)
                # tree.addProdution(log_mon_node)
                tree.logMon = log_mon_node

                log_expr_node = self._log_expr_()
                # print('log_expr_node {0}'.format(log_expr_node))
                # print('~~~~~~~~~~~~~~\n')
                if log_expr_node:
                    # tree.add_child(log_expr_node)
                    # tree.addProdution(log_expr_node)
                    tree.logExpression_ = log_expr_node
                return tree

        return None

    def _log_mon(self):
        # print('_log_mon')
        # tree = ParseTree("log mon")
        tree = LogMon()

        sec_expr_node = self._sec_expr()
        # print('_log_mon() -> _sec_expr(): {0}'.format(sec_expr_node)) # @
        # print('-----------------')
        if sec_expr_node:
            # tree.add_child(sec_expr_node)
            # tree.addProdution(sec_expr_node)
            tree.secExpression = sec_expr_node

        log_mon_node_ = self._log_mon_()
        # print('_log_mon() -> _log_mon_(): {0}'.format(log_mon_node_))
        # print('~~~~~~~~~~~~~~\n')
        if log_mon_node_ is not None:
            # tree.add_child(log_mon_node_)
            # tree.addProdution(log_mon_node_)
            tree.logMon_ = log_mon_node_

        if tree.secExpression or tree.logMon_:
            return tree

        return None

    def _log_mon_(self):
        # print('_log_mon_')
        if self._out_of_range():
            return None

        # tree = ParseTree("log mon'")
        tree = LogMon_()

        if self.string[self.index] == "&":
            self.index += 1
            # tree.add_child(ParseTree("&"))
            # tree.addProdution(LogOperation('&'))
            tree.logOperation = LogOperation('&')

            sec_expr_node = self._sec_expr()
            # print('sec_expr_node {0}'.format(sec_expr_node))
            # print('-----------------')

            if sec_expr_node:
                # tree.add_child(sec_expr_node)
                # tree.addProdution(sec_expr_node)
                tree.secExpression = sec_expr_node

                log_mon_node_ = self._log_mon_()
                # print('log_mon_node_ {0}'.format(log_mon_node_))
                # print('~~~~~~~~~~~~~~\n')
                if log_mon_node_:
                    # tree.add_child(log_mon_node_)
                    # tree.addProdution(log_mon_node_)
                    tree.logMon_ = log_mon_node_

                return tree

        return None

    def _sec_expr(self):
        # print('_sec_expr')
        # tree = ParseTree("sec_expr")

        tree = SecExpr()

        first_exp_node = self._first_expr()
        # print('_sec_expr() -> _first_expr(): {0}'.format(first_exp_node))
        # print('-----------------')
        if first_exp_node:
            # tree.add_child(first_exp_node)
            # tree.addFirstProdution(first_exp_node)
            tree.firtExpression = first_exp_node
            return tree

        if self._out_of_range():
            return None

        if self.string[self.index] == "~":
            self.index += 1
            # print('_sec_expr() -> ~') # @
            # tree.add_child(ParseTree("~"))
            # tree.addSecondProdution(LogOperation('~'))
            tree.logOperation = LogOperation('~')

            first_exp_node = self._first_expr()
            # print('_sec_expr() -> _first_expr(): {0}'.format(first_exp_node)) # @ 
            # print('~~~~~~~~~~~~~~\n')
            if first_exp_node:
                # tree.add_child(first_exp_node)
                # tree.addSecondProdution(first_exp_node)
                tree.firtExpression = first_exp_node
                return tree

        return None

    def _first_expr(self):
        # print('_first_expr')
        tree = ParseTree("first_expr")

        tree = FisrtExpr()

        log_value_node = self._log_value()
        # print('log_value_node {0}'.format(log_value_node))
        # print('-----------------')
        if log_value_node:
            # tree.add_child(log_value_node)
            # tree.addFirstProdution(log_value_node)
            tree.logValue = log_value_node
            return tree

        identifier_node = self._identifier()
        # print('_first_expr() -> _identifier(): {0}'.format(identifier_node)) # @
        # print('~~~~~~~~~~~~~~\n')
        if identifier_node:
            # tree.add_child(identifier_node)
            # tree.addSecondProdution(identifier_node)
            tree.indetificator = identifier_node
            return tree

        return None

    def _log_value(self):
        # print('_log_value')
        tree = ParseTree("log value")

        tree = LogValue()

        if self.string[self.index: self.index + 4] == "true":
            self.index += 4
            # print('log_value_node {0}'.format('true'))
            # print('-----------------')
            # tree.add_child(ParseTree("true"))
            # tree.addProdution('true')
            tree.value = 'true'
            return tree

        if self.string[self.index: self.index + 5] == "false":
            self.index += 5
            # print('identifier_node {0}'.format('false'))
            # print('~~~~~~~~~~~~~~\n')
            # tree.add_child(ParseTree("false"))
            # tree.addProdution('false')
            tree.value = 'false'
            return tree

        return None

    def _identifier(self):
        # print('_identifier')
        # tree = ParseTree("identifier")
        tree = Identifier()
        count = 0
        while True:
            # print(count)
            if self._out_of_range():
                break
            if self.string[self.index] in self.identifiers:
                self.index += 1
                count += 1
            else:
                break

        if count:
            # tree.add_child(ParseTree(self.string[self.index-count: self.index]))
            # tree.addProdution(self.string[self.index-count: self.index])
            tree.value = self.string[self.index-count: self.index]
            return tree

        return None

    def _out_of_range(self):
        return self.index > (len(self.string) - 1)

    def _string_is_end(self):
        # print(self.index, len(self.string))
        return self.index == len(self.string)

    def __repr__(self):
        return f"{self.index}"


if __name__ == "__main__":
    string = "false & ~ A ! ~true & B & C"
    # string = "~A | C"
    print(string)
    p = Parser(string)

    p.accept_string()
    tree = p.get_tree()
    print('hi')