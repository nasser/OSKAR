class Csg(object):
    def __init__(self, terms):
        self.terms = terms
    def debug_data(self):
        return ('Csg', [t.debug_data() for t in self.terms])

class CsgTerm(object):
    def __init__(self, operator, term):
        self.operator = operator
        self.term = term
    def debug_data(self):
        return ('CsgTerm', self.operator.debug_data(), self.term.debug_data())

class CsgFactor(object):
    def __init__(self, lhs, term):
        self.lhs = lhs
        self.term = term
    def debug_data(self):
        return ('CsgFactor',
            self.lhs.debug_data(),
            self.term.debug_data())

class FunctionDefinition(object):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body
    def debug_data(self):
        return ('FunctionDefinition',
            self.name.debug_data(),
            [p.debug_data() for p in self.parameters],
            self.body.debug_data())

class VariableDefinition(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def debug_data(self):
        return ('VariableDefinition',
            self.name.debug_data(),
            self.value.debug_data())

class PictureDefinition(object):
    def __init__(self, name, parameters, body, csg):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.csg = csg

    def debug_data(self):
        return ('PictureDefinition',
            self.name.debug_data(),
            [p.debug_data() for p in self.parameters],
            self.body.debug_data(),
            self.csg.debug_data())

class PictureListDefinition(object):
    def __init__(self, name, parameters, list):
        self.name = name
        self.parameters = parameters
        self.list = list

    def debug_data(self):
        return ('PictureListDefinition',
            self.name.debug_data(),
            [p.debug_data() for p in self.parameters],
            [l.debug_data() for l in self.list])

class Identifier(object):
    def __init__(self, str):
        self.str = str.strip()
    def debug_data(self):
        return ('Identifier', self.str)

class DefaultValueArgument(object):
    def __init__(self):
        pass
    def debug_data(self):
        return ('DefaultValueArgument',)

class Parameter(object):
    def __init__(self, identifier, default_value):
        self.identifier = identifier
        self.default_value = default_value
    def debug_data(self):
        if self.default_value is None:
            return ('Parameter', self.identifier.debug_data())
        else:
            return ('Parameter',
                self.identifier.debug_data(),
                self.default_value.debug_data())

class NamedArgument(object):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def debug_data(self):
        return ('NamedArgument',
            self.identifier.debug_data(),
            self.expression.debug_data())

class Literal(object):
    def __init__(self, val):
        self.val = val
    def debug_data(self):
        return ('Literal', self.val)

class Operator(object):
    def __init__(self, symbol):
        self.symbol = symbol.strip()
    def debug_data(self):
        return ('Operator', self.symbol)

class Infix(object):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    def debug_data(self):
        return ('Infix',
            self.lhs.debug_data(),
            self.op.debug_data(),
            self.rhs.debug_data())

class Invocation(object):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments
    def debug_data(self):
        return ('Invocation',
            self.identifier.debug_data(),
            [a.debug_data() for a in self.arguments])

class NumPics(object):
    def __init__(self, value):
        self.value = value
    def debug_data(self):
        return ('NumPics', self.value.debug_data())

class Transformation(object):
    def __init__(self, operator, arguments):
        self.operator = operator
        self.arguments = arguments
    def debug_data(self):
        return ('Transformation',
            self.operator.debug_data(),
            [a.debug_data() for a in self.arguments])

class TransformSet(object):
    def __init__(self, num_pics, transformations):
        self.num_pics = num_pics
        self.transformations = transformations
    def debug_data(self):
        return ('TransformSet',
            self.num_pics.debug_data(),
            [t.debug_data() for t in self.transformations])

class PictureSet(object):
    def __init__(self, basis, num_pics, transformations):
        self.basis = basis
        self.num_pics = num_pics
        self.transformations = transformations
    def debug_data(self):
        return ('PictureSet',
            self.basis.debug_data(),
            self.num_pics.debug_data(),
            [t.debug_data() for t in self.transformations])

class PictureSetRhs(object):
    def __init__(self, picture_set, transform_set):
        self.picture_set = picture_set
        self.transform_set = transform_set
    def debug_data(self):
        return ('PictureSetRhs',
            self.picture_set.debug_data(),
            [t.debug_data() for t in self.transform_set])

# return node_types.CsgComponent(tree.csg_operator, tree.picture_component)
class CsgComponent(object):
    def __init__(self, csg_operator, picture_component):
        self.csg_operator = csg_operator
        self.picture_component = picture_component
    def debug_data(self):
        return ('CsgComponent',
            self.csg_operator.debug_data(),
            self.picture_component.debug_data())
