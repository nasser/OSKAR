import node_types

class Actions(object):
    def ignore(self, input, start, end, tree):
        return None

    def empty_list(self, input, start, end, tree):
        return []

    def function_definition(self, input, start, end, tree):
        return node_types.FunctionDefinition(tree.identifier,
            tree.parameters,
            tree.expression)

    def identifier(self, input, start, end, tree):
        return node_types.Identifier(input[start:end])

    def expression(self, input, start, end, tree):
        return tree.expression

    def literal(self, input, start, end, tree):
        return node_types.Literal(tree.number)

    def operator(self, input, start, end, tree):
        return node_types.Operator(input[start:end])

    def invocation(self, input, start, end, tree):
        return node_types.Invocation(tree.identifier, tree.arguments)

    def parameter(self, input, start, end, tree):
        if len(tree.default.elements) == 0:
            return node_types.Parameter(tree.identifier, None)
        else:
            return node_types.Parameter(tree.identifier, tree.default.literal)

    def parameters(self, input, start, end, tree):
        return [tree.parameters.first] + [e.parameter for e in tree.parameters.rest.elements]

    def arguments(self, input, start, end, tree):
        return [tree.expressions.first or node_types.DefaultValueArgument()] + [e.expression or node_types.DefaultValueArgument() for e in tree.expressions.rest.elements]

    def number(self, input, start, end, tree):
        return float(input[start:end])

    def infix(self, input, start, end, tree):
        return node_types.Infix(tree.lhs, tree.operator, tree.rhs)

    def variable_definition(self, input, start, end, tree):
        return node_types.VariableDefinition(tree.identifier, tree.expression)

    def picture_definition(self, input, start, end, tree):
        return node_types.PictureDefinition(tree.identifier,
            tree.parameters,
            tree.body,
            tree.csg.elements)

    def num_pics(self, input, start, end, tree):
        return node_types.NumPics(tree.value)

    def transformation(self, input, start, end, tree):
        return node_types.Transformation(tree.operator, tree.arguments)

    def transform_set(self, input, start, end, tree):
        return node_types.TransformSet(tree.num_pics, tree.transformations)

    def picture_set(self, input, start, end, tree):
        return node_types.PictureSet(tree.basis, tree.num_pics, tree.transformations.elements)

    def picture_set_rhs(self, input, start, end, tree):
        return node_types.PictureSetRhs(tree.picture_set, tree.transform_set.elements)

    def csg_component(self, input, start, end, tree):
        return node_types.CsgComponent(tree.csg_operator, tree.picture_component)
