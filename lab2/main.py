import argparse


from grammar_converter import GrammarConverter
from grammar_file import GrammarFile


def process_grammar(filename, action):
    try:
        g = GrammarFile.create_grammar_from_file(filename)
    except Exception as e:
        print(e)
    else:
        print("Loaded grammar:\n{}".format(g))
        if action == "form":
            grammar = GrammarConverter.make_chomsky_form(g)
            # GrammarFile.save_grammar_to_file(grammar, "grammar_without_eps_productions.json")
            # print("\nWithout eps productions:\n{}".format(grammar))
        elif action == "left-rec":
            grammar = GrammarConverter.delete_left_recursion(g)
            GrammarFile.save_grammar_to_file(grammar, "grammar_without_recursion.json")
            print("\nWithout left recursion:\n{}".format(grammar))
        else:
            raise Exception("Unknown type of action")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove eps-productions and left recursion")
    parser.add_argument("action", type=str, choices=["form", "left-rec"], help="form or left-rec")
    parser.add_argument("filename", type=str, help="File with grammar")
    args = parser.parse_args()
    process_grammar(args.filename, args.action)

