import sys
import traceback
import grammar
import actions
import pprint
import ast
import astor

# TODO commit
# TODO commit, push, PR canopy hack

def stringify(tree, indent=0):
    if(isinstance(tree, grammar.TreeNode)):
        if(len(tree.elements) == 0):
            return (" " * indent) + "\"" + tree.text + "\""
        return (" " * indent) + "<" + tree.text + ">\n" + ("\n".join([stringify(x, indent+1) for x in tree.elements if x is not None]) + "\n" + (" " * indent) + "</" + tree.text + ">")
    else:
        return (" " * indent) + str(tree)

with open(sys.argv[2], "w") as f:
    log_file = f
    with open(sys.argv[1], "r") as f:
        example_source = f.read().strip()
        parse_tree = ""
        errors = ""
        try:
            parsed = grammar.parse(example_source, actions=actions.Actions())
            parse_tree = pprint.pformat([e.debug_data() for e in parsed.elements]).replace(",", "").replace("'", "")
            print("OK")
        except Exception:
            errors = traceback.format_exc()
            print("Failed")
        log_file.write("--- source\n")
        log_file.write(example_source)
        log_file.write("\n--- parse tree\n")
        log_file.write(parse_tree)
        log_file.write("\n--- errors\n")
        log_file.write(errors)
        log_file.write("\n--- parser test\n")
        log_file.write(astor.to_source(ast.Call(ast.Name(sys.argv[1]), [ast.Name(sys.argv[1])], [])))
