from parsimonious.grammar import Grammar
import sys

# optional transform arguments?

with open("grammar.peg", "r") as f:
    grammar_source = f.read()
    grammar = Grammar(grammar_source)

with open(sys.argv[1], "r") as f:
    example_source = f.read().strip()
    parsed = grammar.parse(example_source)
    print(example_source)
    print(parsed)
