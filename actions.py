import node_types

class Actions(object):
    def ignore(self, input, start, end, tree):
        return None

    def function_definition(self, input, start, end, tree):
        return node_types.FunctionDefinition(tree.identifier, tree.parameters, tree.expression)

    def identifier(self, input, start, end, tree):
        return node_types.Identifier(input[start:end])

    def expression(self, input, start, end, tree):
        return tree.expression

    def literal(self, input, start, end, tree):
        return node_types.Literal(tree.number)

    def operator(self, input, start, end, tree):
        return node_types.Operator(input[start:end])

    def parameter(self, input, start, end, tree):
        if len(tree.default.elements) == 0:
            return node_types.Parameter(tree.identifier, None)
        else:
            return node_types.Parameter(elements[0])

    def parameters(self, input, start, end, tree):
        params = [tree.parameters.first] + [e.parameter for e in tree.parameters.rest.elements]
        return node_types.Parameters(params)

    def number(self, input, start, end, tree):
        return float(input[start:end])

    def infix(self, input, start, end, tree):
        return node_types.Infix(tree.lhs, tree.operator, tree.rhs)
