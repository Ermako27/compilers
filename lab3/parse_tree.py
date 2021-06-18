class ParseTree:
    def __init__(self, value):
        self.value = value
        self.childs = []

    def add_child(self, child):
        self.childs.append(child)

    def __repr__(self):
        return f"{self.value} -> {[child.value for child in self.childs]}"


def print_tree(tree: ParseTree, indent=0):
    indent_str = "----|" * indent + "> "
    if tree.childs:
        print(indent_str + f"{tree.value}")
        for child in tree.childs:
            print_tree(child, indent + 1)
    else:
        print(indent_str + f"({tree.value})")
