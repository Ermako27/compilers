# from parse_tree import print_tree
from parser import Parser

if __name__ == "__main__":
    string = "false & ~ A ! ~true & B & C"
    # string = "~A | C"
    print(string)
    p = Parser(string)

    p.accept_string()
    tree = p.get_tree()
    print('hi')
    # if p.accept_string():
    #     # print(p.get_tree())
    #     # print('~~~~~~~~~~~~~~~~\n')
    #     tree = p.get_tree()

    #     print_tree(p.get_tree())
