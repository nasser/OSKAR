# This file was generated from grammar.peg
# See http://canopy.jcoglan.com/ for documentation.

from collections import defaultdict
import re


class TreeNode(object):
    def __init__(self, text, offset, elements=None):
        self.text = text
        self.offset = offset
        self.elements = elements or []

    def __iter__(self):
        for el in self.elements:
            yield el


class TreeNode1(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode1, self).__init__(text, offset, elements)
        self._ = elements[0]
        self.expr = elements[1]


class TreeNode2(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode2, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self.parameters = elements[1]
        self._ = elements[3]
        self.expression = elements[4]


class TreeNode3(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode3, self).__init__(text, offset, elements)
        self._ = elements[4]
        self.parameters = elements[2]


class TreeNode4(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode4, self).__init__(text, offset, elements)
        self.first = elements[0]
        self.parameter = elements[0]
        self.rest = elements[1]


class TreeNode5(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode5, self).__init__(text, offset, elements)
        self._ = elements[1]
        self.parameter = elements[2]


class TreeNode6(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode6, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self.default = elements[1]


class TreeNode7(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode7, self).__init__(text, offset, elements)
        self._ = elements[1]
        self.literal = elements[2]


class TreeNode8(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode8, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self._ = elements[2]
        self.expression = elements[3]


class TreeNode9(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode9, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self.parameters = elements[1]
        self._ = elements[3]
        self.body = elements[4]
        self.picture_component = elements[4]
        self.csg = elements[5]


class TreeNode10(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode10, self).__init__(text, offset, elements)
        self.terms = elements[0]
        self._ = elements[1]


class TreeNode11(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode11, self).__init__(text, offset, elements)
        self.operator = elements[0]
        self.csg_operator = elements[0]
        self.term = elements[1]
        self.csg_factor = elements[1]


class TreeNode12(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode12, self).__init__(text, offset, elements)
        self._ = elements[5]
        self.lhs = elements[2]
        self.picture_component = elements[2]
        self.term = elements[3]
        self.csg_term = elements[3]


class TreeNode13(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode13, self).__init__(text, offset, elements)
        self.picture_component = elements[0]
        self._ = elements[1]


class TreeNode14(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode14, self).__init__(text, offset, elements)
        self._ = elements[1]


class TreeNode15(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode15, self).__init__(text, offset, elements)
        self.picture_set = elements[0]
        self.transform_set = elements[1]


class TreeNode16(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode16, self).__init__(text, offset, elements)
        self._ = elements[6]
        self.basis = elements[2]
        self.num_pics = elements[3]
        self.transformations = elements[4]


class TreeNode17(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode17, self).__init__(text, offset, elements)
        self._ = elements[5]
        self.num_pics = elements[2]
        self.transformations = elements[3]


class TreeNode18(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode18, self).__init__(text, offset, elements)
        self.value = elements[1]
        self._ = elements[3]


class TreeNode19(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode19, self).__init__(text, offset, elements)
        self.operator = elements[0]
        self.arguments = elements[1]


class TreeNode20(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode20, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self.parameters = elements[1]
        self._ = elements[3]
        self.picture_list = elements[4]


class TreeNode21(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode21, self).__init__(text, offset, elements)
        self._ = elements[4]
        self.pictures = elements[2]


class TreeNode22(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode22, self).__init__(text, offset, elements)
        self.first = elements[0]
        self.identifier = elements[0]
        self.rest = elements[1]


class TreeNode23(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode23, self).__init__(text, offset, elements)
        self._ = elements[1]
        self.identifier = elements[2]


class TreeNode24(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode24, self).__init__(text, offset, elements)
        self.expression = elements[0]
        self.semicolon = elements[1]


class TreeNode25(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode25, self).__init__(text, offset, elements)
        self.lhs = elements[0]
        self.term = elements[0]
        self.op = elements[1]
        self.operator = elements[1]
        self.rhs = elements[2]
        self.expression = elements[2]


class TreeNode26(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode26, self).__init__(text, offset, elements)
        self._ = elements[4]
        self.expression = elements[2]


class TreeNode27(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode27, self).__init__(text, offset, elements)
        self._ = elements[1]


class TreeNode28(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode28, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self.arguments = elements[1]


class TreeNode29(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode29, self).__init__(text, offset, elements)
        self._ = elements[4]
        self.arguments = elements[2]


class TreeNode30(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode30, self).__init__(text, offset, elements)
        self.first = elements[0]
        self.rest = elements[1]


class TreeNode31(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode31, self).__init__(text, offset, elements)
        self._ = elements[1]
        self.argument = elements[2]


class TreeNode32(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode32, self).__init__(text, offset, elements)
        self.identifier = elements[0]
        self._ = elements[2]
        self.expression = elements[3]


class TreeNode33(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode33, self).__init__(text, offset, elements)
        self._ = elements[3]


class TreeNode34(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode34, self).__init__(text, offset, elements)
        self.number = elements[0]
        self._ = elements[1]


class TreeNode35(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode35, self).__init__(text, offset, elements)
        self.symbol = elements[1]
        self._ = elements[2]


class TreeNode36(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode36, self).__init__(text, offset, elements)
        self.digits = elements[0]
        self._ = elements[1]


class TreeNode37(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode37, self).__init__(text, offset, elements)
        self._ = elements[1]


class TreeNode38(TreeNode):
    def __init__(self, text, offset, elements):
        super(TreeNode38, self).__init__(text, offset, elements)
        self.whitespace = elements[2]


class ParseError(SyntaxError):
    pass


FAILURE = object()


class Grammar(object):
    REGEX_1 = re.compile('^[\\+\\*\\/\\-\\@]')
    REGEX_2 = re.compile('^[^\\s(),#=\\*\\+\\-\\[\\]]')
    REGEX_3 = re.compile('^[0-9\\.]')
    REGEX_4 = re.compile('^[\\n\\s]')
    REGEX_5 = re.compile('^[^\\n]')

    def _read_start(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['start'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            address1 = self._read_top_level()
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['start'][index0] = (address0, self._offset)
        return address0

    def _read_top_level(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['top_level'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read__()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_function_definition()
            if address2 is FAILURE:
                self._offset = index2
                address2 = self._read_variable_definition()
                if address2 is FAILURE:
                    self._offset = index2
                    address2 = self._read_picture_list_definition()
                    if address2 is FAILURE:
                        self._offset = index2
                        address2 = self._read_picture_definition()
                        if address2 is FAILURE:
                            self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.top_level(self._input, index1, self._offset, TreeNode1(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['top_level'][index0] = (address0, self._offset)
        return address0

    def _read_function_definition(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['function_definition'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_parameters()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 1]
                if chunk0 == '=':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"="')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_expression()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.function_definition(self._input, index1, self._offset, TreeNode2(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['function_definition'][index0] = (address0, self._offset)
        return address0

    def _read_parameters(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['parameters'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_empty_arguments()
        if address0 is FAILURE:
            self._offset = index1
            index2, elements0 = self._offset, []
            address1 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == '(':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"("')
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                address2 = self._read__()
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    index4, elements1 = self._offset, []
                    address4 = FAILURE
                    address4 = self._read_parameter()
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        address5 = FAILURE
                        remaining0, index5, elements2, address6 = 0, self._offset, [], True
                        while address6 is not FAILURE:
                            index6, elements3 = self._offset, []
                            address7 = FAILURE
                            chunk1 = None
                            if self._offset < self._input_size:
                                chunk1 = self._input[self._offset:self._offset + 1]
                            if chunk1 == ',':
                                address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address7 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('","')
                            if address7 is not FAILURE:
                                elements3.append(address7)
                                address8 = FAILURE
                                address8 = self._read__()
                                if address8 is not FAILURE:
                                    elements3.append(address8)
                                    address9 = FAILURE
                                    address9 = self._read_parameter()
                                    if address9 is not FAILURE:
                                        elements3.append(address9)
                                    else:
                                        elements3 = None
                                        self._offset = index6
                                else:
                                    elements3 = None
                                    self._offset = index6
                            else:
                                elements3 = None
                                self._offset = index6
                            if elements3 is None:
                                address6 = FAILURE
                            else:
                                address6 = TreeNode5(self._input[index6:self._offset], index6, elements3)
                                self._offset = self._offset
                            if address6 is not FAILURE:
                                elements2.append(address6)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address5 = TreeNode(self._input[index5:self._offset], index5, elements2)
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements1.append(address5)
                        else:
                            elements1 = None
                            self._offset = index4
                    else:
                        elements1 = None
                        self._offset = index4
                    if elements1 is None:
                        address3 = FAILURE
                    else:
                        address3 = TreeNode4(self._input[index4:self._offset], index4, elements1)
                        self._offset = self._offset
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3)
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address10 = FAILURE
                        chunk2 = None
                        if self._offset < self._input_size:
                            chunk2 = self._input[self._offset:self._offset + 1]
                        if chunk2 == ')':
                            address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address10 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('")"')
                        if address10 is not FAILURE:
                            elements0.append(address10)
                            address11 = FAILURE
                            address11 = self._read__()
                            if address11 is not FAILURE:
                                elements0.append(address11)
                            else:
                                elements0 = None
                                self._offset = index2
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = self._actions.parameters(self._input, index2, self._offset, TreeNode3(self._input[index2:self._offset], index2, elements0))
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
        self._cache['parameters'][index0] = (address0, self._offset)
        return address0

    def _read_parameter(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['parameter'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            index3, elements1 = self._offset, []
            address3 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == '=':
                address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address3 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"="')
            if address3 is not FAILURE:
                elements1.append(address3)
                address4 = FAILURE
                address4 = self._read__()
                if address4 is not FAILURE:
                    elements1.append(address4)
                    address5 = FAILURE
                    address5 = self._read_literal()
                    if address5 is not FAILURE:
                        elements1.append(address5)
                    else:
                        elements1 = None
                        self._offset = index3
                else:
                    elements1 = None
                    self._offset = index3
            else:
                elements1 = None
                self._offset = index3
            if elements1 is None:
                address2 = FAILURE
            else:
                address2 = TreeNode7(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.parameter(self._input, index1, self._offset, TreeNode6(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['parameter'][index0] = (address0, self._offset)
        return address0

    def _read_variable_definition(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['variable_definition'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == '=':
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"="')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read__()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_expression()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.variable_definition(self._input, index1, self._offset, TreeNode8(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['variable_definition'][index0] = (address0, self._offset)
        return address0

    def _read_picture_definition(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_definition'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_parameters()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 2]
                if chunk0 == '<<':
                    address3 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                    self._offset = self._offset + 2
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"<<"')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_picture_component()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read_csg()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.picture_definition(self._input, index1, self._offset, TreeNode9(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['picture_definition'][index0] = (address0, self._offset)
        return address0

    def _read_csg(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['csg'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        remaining0, index2, elements1, address2 = 0, self._offset, [], True
        while address2 is not FAILURE:
            address2 = self._read_csg_term()
            if address2 is not FAILURE:
                elements1.append(address2)
                remaining0 -= 1
        if remaining0 <= 0:
            address1 = TreeNode(self._input[index2:self._offset], index2, elements1)
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address3 = FAILURE
            address3 = self._read__()
            if address3 is not FAILURE:
                elements0.append(address3)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.csg(self._input, index1, self._offset, TreeNode10(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['csg'][index0] = (address0, self._offset)
        return address0

    def _read_csg_term(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['csg_term'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_csg_operator()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_csg_factor()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.csg_term(self._input, index1, self._offset, TreeNode11(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['csg_term'][index0] = (address0, self._offset)
        return address0

    def _read_csg_factor(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['csg_factor'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_picture_component()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_csg_term()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 1]
                        if chunk1 == ')':
                            address5 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address5 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('")"')
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address6 = FAILURE
                            address6 = self._read__()
                            if address6 is not FAILURE:
                                elements0.append(address6)
                            else:
                                elements0 = None
                                self._offset = index2
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.csg_factor(self._input, index2, self._offset, TreeNode12(self._input[index2:self._offset], index2, elements0))
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            index3, elements1 = self._offset, []
            address7 = FAILURE
            address7 = self._read_picture_component()
            if address7 is not FAILURE:
                elements1.append(address7)
                address8 = FAILURE
                address8 = self._read__()
                if address8 is not FAILURE:
                    elements1.append(address8)
                else:
                    elements1 = None
                    self._offset = index3
            else:
                elements1 = None
                self._offset = index3
            if elements1 is None:
                address0 = FAILURE
            else:
                address0 = self._actions.csg_picture_component(self._input, index3, self._offset, TreeNode13(self._input[index3:self._offset], index3, elements1))
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
        self._cache['csg_factor'][index0] = (address0, self._offset)
        return address0

    def _read_csg_operator(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['csg_operator'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 2]
        if chunk0 == '++':
            address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
            self._offset = self._offset + 2
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"++"')
        if address1 is FAILURE:
            self._offset = index2
            chunk1 = None
            if self._offset < self._input_size:
                chunk1 = self._input[self._offset:self._offset + 2]
            if chunk1 == '--':
                address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                self._offset = self._offset + 2
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"--"')
            if address1 is FAILURE:
                self._offset = index2
                chunk2 = None
                if self._offset < self._input_size:
                    chunk2 = self._input[self._offset:self._offset + 2]
                if chunk2 == '&&':
                    address1 = TreeNode(self._input[self._offset:self._offset + 2], self._offset)
                    self._offset = self._offset + 2
                else:
                    address1 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"&&"')
                if address1 is FAILURE:
                    self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.operator(self._input, index1, self._offset, TreeNode14(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['csg_operator'][index0] = (address0, self._offset)
        return address0

    def _read_picture_component(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_component'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_picture_set_rhs()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_invocation()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['picture_component'][index0] = (address0, self._offset)
        return address0

    def _read_picture_set_rhs(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_set_rhs'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_picture_set()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                address3 = self._read_transform_set()
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.picture_set_rhs(self._input, index1, self._offset, TreeNode15(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['picture_set_rhs'][index0] = (address0, self._offset)
        return address0

    def _read_picture_set(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_set'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '[':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"["')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_basis()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_num_pics()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        remaining0, index2, elements1, address6 = 0, self._offset, [], True
                        while address6 is not FAILURE:
                            address6 = self._read_transformation()
                            if address6 is not FAILURE:
                                elements1.append(address6)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address5 = TreeNode(self._input[index2:self._offset], index2, elements1)
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements0.append(address5)
                            address7 = FAILURE
                            chunk1 = None
                            if self._offset < self._input_size:
                                chunk1 = self._input[self._offset:self._offset + 1]
                            if chunk1 == ']':
                                address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address7 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('"]"')
                            if address7 is not FAILURE:
                                elements0.append(address7)
                                address8 = FAILURE
                                address8 = self._read__()
                                if address8 is not FAILURE:
                                    elements0.append(address8)
                                else:
                                    elements0 = None
                                    self._offset = index1
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.picture_set(self._input, index1, self._offset, TreeNode16(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['picture_set'][index0] = (address0, self._offset)
        return address0

    def _read_transform_set(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['transform_set'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '[':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"["')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_num_pics()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    remaining0, index2, elements1, address5 = 0, self._offset, [], True
                    while address5 is not FAILURE:
                        address5 = self._read_transformation()
                        if address5 is not FAILURE:
                            elements1.append(address5)
                            remaining0 -= 1
                    if remaining0 <= 0:
                        address4 = TreeNode(self._input[index2:self._offset], index2, elements1)
                        self._offset = self._offset
                    else:
                        address4 = FAILURE
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address6 = FAILURE
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 1]
                        if chunk1 == ']':
                            address6 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address6 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('"]"')
                        if address6 is not FAILURE:
                            elements0.append(address6)
                            address7 = FAILURE
                            address7 = self._read__()
                            if address7 is not FAILURE:
                                elements0.append(address7)
                            else:
                                elements0 = None
                                self._offset = index1
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.transform_set(self._input, index1, self._offset, TreeNode17(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['transform_set'][index0] = (address0, self._offset)
        return address0

    def _read_basis(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['basis'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_invocation()
        self._cache['basis'][index0] = (address0, self._offset)
        return address0

    def _read_num_pics(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['num_pics'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '{':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"{"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_literal()
            if address2 is FAILURE:
                self._offset = index2
                address2 = self._read_identifier()
                if address2 is FAILURE:
                    self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 == '}':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"}"')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.num_pics(self._input, index1, self._offset, TreeNode18(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['num_pics'][index0] = (address0, self._offset)
        return address0

    def _read_transformation(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['transformation'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_operator()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_arguments()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.transformation(self._input, index1, self._offset, TreeNode19(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['transformation'][index0] = (address0, self._offset)
        return address0

    def _read_picture_list_definition(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_list_definition'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index2 = self._offset
            address2 = self._read_parameters()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index2:index2], index2)
                self._offset = index2
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk0 = None
                if self._offset < self._input_size:
                    chunk0 = self._input[self._offset:self._offset + 3]
                if chunk0 == '<<<':
                    address3 = TreeNode(self._input[self._offset:self._offset + 3], self._offset)
                    self._offset = self._offset + 3
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('"<<<"')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read_picture_list()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.picture_list_definition(self._input, index1, self._offset, TreeNode20(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['picture_list_definition'][index0] = (address0, self._offset)
        return address0

    def _read_picture_list(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['picture_list'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '[':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"["')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                index2 = self._offset
                index3, elements1 = self._offset, []
                address4 = FAILURE
                address4 = self._read_identifier()
                if address4 is not FAILURE:
                    elements1.append(address4)
                    address5 = FAILURE
                    remaining0, index4, elements2, address6 = 0, self._offset, [], True
                    while address6 is not FAILURE:
                        index5, elements3 = self._offset, []
                        address7 = FAILURE
                        chunk1 = None
                        if self._offset < self._input_size:
                            chunk1 = self._input[self._offset:self._offset + 1]
                        if chunk1 == ',':
                            address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address7 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('","')
                        if address7 is not FAILURE:
                            elements3.append(address7)
                            address8 = FAILURE
                            address8 = self._read__()
                            if address8 is not FAILURE:
                                elements3.append(address8)
                                address9 = FAILURE
                                address9 = self._read_identifier()
                                if address9 is not FAILURE:
                                    elements3.append(address9)
                                else:
                                    elements3 = None
                                    self._offset = index5
                            else:
                                elements3 = None
                                self._offset = index5
                        else:
                            elements3 = None
                            self._offset = index5
                        if elements3 is None:
                            address6 = FAILURE
                        else:
                            address6 = TreeNode23(self._input[index5:self._offset], index5, elements3)
                            self._offset = self._offset
                        if address6 is not FAILURE:
                            elements2.append(address6)
                            remaining0 -= 1
                    if remaining0 <= 0:
                        address5 = TreeNode(self._input[index4:self._offset], index4, elements2)
                        self._offset = self._offset
                    else:
                        address5 = FAILURE
                    if address5 is not FAILURE:
                        elements1.append(address5)
                    else:
                        elements1 = None
                        self._offset = index3
                else:
                    elements1 = None
                    self._offset = index3
                if elements1 is None:
                    address3 = FAILURE
                else:
                    address3 = TreeNode22(self._input[index3:self._offset], index3, elements1)
                    self._offset = self._offset
                if address3 is FAILURE:
                    address3 = TreeNode(self._input[index2:index2], index2)
                    self._offset = index2
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address10 = FAILURE
                    chunk2 = None
                    if self._offset < self._input_size:
                        chunk2 = self._input[self._offset:self._offset + 1]
                    if chunk2 == ']':
                        address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address10 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('"]"')
                    if address10 is not FAILURE:
                        elements0.append(address10)
                        address11 = FAILURE
                        address11 = self._read__()
                        if address11 is not FAILURE:
                            elements0.append(address11)
                        else:
                            elements0 = None
                            self._offset = index1
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.picture_list(self._input, index1, self._offset, TreeNode21(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['picture_list'][index0] = (address0, self._offset)
        return address0

    def _read_expression(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['expression'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_infix()
        if address1 is FAILURE:
            self._offset = index2
            address1 = self._read_invocation()
            if address1 is FAILURE:
                self._offset = index2
                address1 = self._read_literal()
                if address1 is FAILURE:
                    self._offset = index2
                    address1 = self._read_identifier()
                    if address1 is FAILURE:
                        self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_semicolon()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.expression(self._input, index1, self._offset, TreeNode24(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['expression'][index0] = (address0, self._offset)
        return address0

    def _read_infix(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['infix'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_term()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_operator()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_expression()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.infix(self._input, index1, self._offset, TreeNode25(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['infix'][index0] = (address0, self._offset)
        return address0

    def _read_term(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['term'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read_expression()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    chunk1 = None
                    if self._offset < self._input_size:
                        chunk1 = self._input[self._offset:self._offset + 1]
                    if chunk1 == ')':
                        address4 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                        self._offset = self._offset + 1
                    else:
                        address4 = FAILURE
                        if self._offset > self._failure:
                            self._failure = self._offset
                            self._expected = []
                        if self._offset == self._failure:
                            self._expected.append('")"')
                    if address4 is not FAILURE:
                        elements0.append(address4)
                        address5 = FAILURE
                        address5 = self._read__()
                        if address5 is not FAILURE:
                            elements0.append(address5)
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode26(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_invocation()
            if address0 is FAILURE:
                self._offset = index1
                address0 = self._read_literal()
                if address0 is FAILURE:
                    self._offset = index1
                    address0 = self._read_identifier()
                    if address0 is FAILURE:
                        self._offset = index1
        self._cache['term'][index0] = (address0, self._offset)
        return address0

    def _read_operator(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['operator'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 is not None and Grammar.REGEX_1.search(chunk0):
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('[\\+\\*\\/\\-\\@]')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.operator(self._input, index1, self._offset, TreeNode27(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['operator'][index0] = (address0, self._offset)
        return address0

    def _read_invocation(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['invocation'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_arguments()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.invocation(self._input, index1, self._offset, TreeNode28(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['invocation'][index0] = (address0, self._offset)
        return address0

    def _read_arguments(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['arguments'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_empty_arguments()
        if address0 is FAILURE:
            self._offset = index1
            index2, elements0 = self._offset, []
            address1 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == '(':
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"("')
            if address1 is not FAILURE:
                elements0.append(address1)
                address2 = FAILURE
                address2 = self._read__()
                if address2 is not FAILURE:
                    elements0.append(address2)
                    address3 = FAILURE
                    index3 = self._offset
                    index4, elements1 = self._offset, []
                    address4 = FAILURE
                    index5 = self._offset
                    address4 = self._read_argument()
                    if address4 is FAILURE:
                        self._offset = index5
                        address4 = self._read__()
                        if address4 is FAILURE:
                            self._offset = index5
                    if address4 is not FAILURE:
                        elements1.append(address4)
                        address5 = FAILURE
                        remaining0, index6, elements2, address6 = 0, self._offset, [], True
                        while address6 is not FAILURE:
                            index7, elements3 = self._offset, []
                            address7 = FAILURE
                            chunk1 = None
                            if self._offset < self._input_size:
                                chunk1 = self._input[self._offset:self._offset + 1]
                            if chunk1 == ',':
                                address7 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                                self._offset = self._offset + 1
                            else:
                                address7 = FAILURE
                                if self._offset > self._failure:
                                    self._failure = self._offset
                                    self._expected = []
                                if self._offset == self._failure:
                                    self._expected.append('","')
                            if address7 is not FAILURE:
                                elements3.append(address7)
                                address8 = FAILURE
                                address8 = self._read__()
                                if address8 is not FAILURE:
                                    elements3.append(address8)
                                    address9 = FAILURE
                                    index8 = self._offset
                                    address9 = self._read_argument()
                                    if address9 is FAILURE:
                                        self._offset = index8
                                        address9 = self._read__()
                                        if address9 is FAILURE:
                                            self._offset = index8
                                    if address9 is not FAILURE:
                                        elements3.append(address9)
                                    else:
                                        elements3 = None
                                        self._offset = index7
                                else:
                                    elements3 = None
                                    self._offset = index7
                            else:
                                elements3 = None
                                self._offset = index7
                            if elements3 is None:
                                address6 = FAILURE
                            else:
                                address6 = TreeNode31(self._input[index7:self._offset], index7, elements3)
                                self._offset = self._offset
                            if address6 is not FAILURE:
                                elements2.append(address6)
                                remaining0 -= 1
                        if remaining0 <= 0:
                            address5 = TreeNode(self._input[index6:self._offset], index6, elements2)
                            self._offset = self._offset
                        else:
                            address5 = FAILURE
                        if address5 is not FAILURE:
                            elements1.append(address5)
                        else:
                            elements1 = None
                            self._offset = index4
                    else:
                        elements1 = None
                        self._offset = index4
                    if elements1 is None:
                        address3 = FAILURE
                    else:
                        address3 = TreeNode30(self._input[index4:self._offset], index4, elements1)
                        self._offset = self._offset
                    if address3 is FAILURE:
                        address3 = TreeNode(self._input[index3:index3], index3)
                        self._offset = index3
                    if address3 is not FAILURE:
                        elements0.append(address3)
                        address10 = FAILURE
                        chunk2 = None
                        if self._offset < self._input_size:
                            chunk2 = self._input[self._offset:self._offset + 1]
                        if chunk2 == ')':
                            address10 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                            self._offset = self._offset + 1
                        else:
                            address10 = FAILURE
                            if self._offset > self._failure:
                                self._failure = self._offset
                                self._expected = []
                            if self._offset == self._failure:
                                self._expected.append('")"')
                        if address10 is not FAILURE:
                            elements0.append(address10)
                            address11 = FAILURE
                            address11 = self._read__()
                            if address11 is not FAILURE:
                                elements0.append(address11)
                            else:
                                elements0 = None
                                self._offset = index2
                        else:
                            elements0 = None
                            self._offset = index2
                    else:
                        elements0 = None
                        self._offset = index2
                else:
                    elements0 = None
                    self._offset = index2
            else:
                elements0 = None
                self._offset = index2
            if elements0 is None:
                address0 = FAILURE
            else:
                address0 = self._actions.arguments(self._input, index2, self._offset, TreeNode29(self._input[index2:self._offset], index2, elements0))
                self._offset = self._offset
            if address0 is FAILURE:
                self._offset = index1
        self._cache['arguments'][index0] = (address0, self._offset)
        return address0

    def _read_argument(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['argument'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        address0 = self._read_named_argument()
        if address0 is FAILURE:
            self._offset = index1
            address0 = self._read_positional_argument()
            if address0 is FAILURE:
                self._offset = index1
        self._cache['argument'][index0] = (address0, self._offset)
        return address0

    def _read_named_argument(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['named_argument'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_identifier()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 == '=':
                address2 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address2 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('"="')
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read__()
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read_expression()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.named_argument(self._input, index1, self._offset, TreeNode32(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['named_argument'][index0] = (address0, self._offset)
        return address0

    def _read_positional_argument(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['positional_argument'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        address0 = self._read_expression()
        self._cache['positional_argument'][index0] = (address0, self._offset)
        return address0

    def _read_empty_arguments(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['empty_arguments'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '(':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"("')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 == ')':
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('")"')
                if address3 is not FAILURE:
                    elements0.append(address3)
                    address4 = FAILURE
                    address4 = self._read__()
                    if address4 is not FAILURE:
                        elements0.append(address4)
                    else:
                        elements0 = None
                        self._offset = index1
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.empty_list(self._input, index1, self._offset, TreeNode33(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['empty_arguments'][index0] = (address0, self._offset)
        return address0

    def _read_literal(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['literal'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_number()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.literal(self._input, index1, self._offset, TreeNode34(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['literal'][index0] = (address0, self._offset)
        return address0

    def _read_identifier(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['identifier'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_number()
        self._offset = index2
        if address1 is FAILURE:
            address1 = TreeNode(self._input[self._offset:self._offset], self._offset)
            self._offset = self._offset
        else:
            address1 = FAILURE
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read_symbol()
            if address2 is not FAILURE:
                elements0.append(address2)
                address3 = FAILURE
                address3 = self._read__()
                if address3 is not FAILURE:
                    elements0.append(address3)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.identifier(self._input, index1, self._offset, TreeNode35(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['identifier'][index0] = (address0, self._offset)
        return address0

    def _read_number(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['number'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        address1 = self._read_digits()
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.number(self._input, index1, self._offset, TreeNode36(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['number'][index0] = (address0, self._offset)
        return address0

    def _read_symbol(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['symbol'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 1, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_2.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[^\\s(),#=\\*\\+\\-\\[\\]]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['symbol'][index0] = (address0, self._offset)
        return address0

    def _read_digits(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['digits'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '-':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"-"')
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2)
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index3, elements1, address3 = 1, self._offset, [], True
            while address3 is not FAILURE:
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 is not None and Grammar.REGEX_3.search(chunk1):
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[0-9\\.]')
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index3:self._offset], index3, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['digits'][index0] = (address0, self._offset)
        return address0

    def _read_semicolon(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['semicolon'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1 = self._offset
        index2, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == ';':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('";"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            address2 = self._read__()
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index2
        else:
            elements0 = None
            self._offset = index2
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode37(self._input[index2:self._offset], index2, elements0)
            self._offset = self._offset
        if address0 is FAILURE:
            address0 = TreeNode(self._input[index1:index1], index1)
            self._offset = index1
        self._cache['semicolon'][index0] = (address0, self._offset)
        return address0

    def _read__(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['_'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        index2 = self._offset
        address1 = self._read_whitespace()
        if address1 is FAILURE:
            address1 = TreeNode(self._input[index2:index2], index2)
            self._offset = index2
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            index3 = self._offset
            address2 = self._read_comment()
            if address2 is FAILURE:
                address2 = TreeNode(self._input[index3:index3], index3)
                self._offset = index3
            if address2 is not FAILURE:
                elements0.append(address2)
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = self._actions.ignore(self._input, index1, self._offset, TreeNode(self._input[index1:self._offset], index1, elements0))
            self._offset = self._offset
        self._cache['_'][index0] = (address0, self._offset)
        return address0

    def _read_whitespace(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['whitespace'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        remaining0, index1, elements0, address1 = 0, self._offset, [], True
        while address1 is not FAILURE:
            chunk0 = None
            if self._offset < self._input_size:
                chunk0 = self._input[self._offset:self._offset + 1]
            if chunk0 is not None and Grammar.REGEX_4.search(chunk0):
                address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                self._offset = self._offset + 1
            else:
                address1 = FAILURE
                if self._offset > self._failure:
                    self._failure = self._offset
                    self._expected = []
                if self._offset == self._failure:
                    self._expected.append('[\\n\\s]')
            if address1 is not FAILURE:
                elements0.append(address1)
                remaining0 -= 1
        if remaining0 <= 0:
            address0 = TreeNode(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        else:
            address0 = FAILURE
        self._cache['whitespace'][index0] = (address0, self._offset)
        return address0

    def _read_comment(self):
        address0, index0 = FAILURE, self._offset
        cached = self._cache['comment'].get(index0)
        if cached:
            self._offset = cached[1]
            return cached[0]
        index1, elements0 = self._offset, []
        address1 = FAILURE
        chunk0 = None
        if self._offset < self._input_size:
            chunk0 = self._input[self._offset:self._offset + 1]
        if chunk0 == '#':
            address1 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
            self._offset = self._offset + 1
        else:
            address1 = FAILURE
            if self._offset > self._failure:
                self._failure = self._offset
                self._expected = []
            if self._offset == self._failure:
                self._expected.append('"#"')
        if address1 is not FAILURE:
            elements0.append(address1)
            address2 = FAILURE
            remaining0, index2, elements1, address3 = 0, self._offset, [], True
            while address3 is not FAILURE:
                chunk1 = None
                if self._offset < self._input_size:
                    chunk1 = self._input[self._offset:self._offset + 1]
                if chunk1 is not None and Grammar.REGEX_5.search(chunk1):
                    address3 = TreeNode(self._input[self._offset:self._offset + 1], self._offset)
                    self._offset = self._offset + 1
                else:
                    address3 = FAILURE
                    if self._offset > self._failure:
                        self._failure = self._offset
                        self._expected = []
                    if self._offset == self._failure:
                        self._expected.append('[^\\n]')
                if address3 is not FAILURE:
                    elements1.append(address3)
                    remaining0 -= 1
            if remaining0 <= 0:
                address2 = TreeNode(self._input[index2:self._offset], index2, elements1)
                self._offset = self._offset
            else:
                address2 = FAILURE
            if address2 is not FAILURE:
                elements0.append(address2)
                address4 = FAILURE
                address4 = self._read_whitespace()
                if address4 is not FAILURE:
                    elements0.append(address4)
                else:
                    elements0 = None
                    self._offset = index1
            else:
                elements0 = None
                self._offset = index1
        else:
            elements0 = None
            self._offset = index1
        if elements0 is None:
            address0 = FAILURE
        else:
            address0 = TreeNode38(self._input[index1:self._offset], index1, elements0)
            self._offset = self._offset
        self._cache['comment'][index0] = (address0, self._offset)
        return address0


class Parser(Grammar):
    def __init__(self, input, actions, types):
        self._input = input
        self._input_size = len(input)
        self._actions = actions
        self._types = types
        self._offset = 0
        self._cache = defaultdict(dict)
        self._failure = 0
        self._expected = []

    def parse(self):
        tree = self._read_start()
        if tree is not FAILURE and self._offset == self._input_size:
            return tree
        if not self._expected:
            self._failure = self._offset
            self._expected.append('<EOF>')
        raise ParseError(format_error(self._input, self._failure, self._expected))


def format_error(input, offset, expected):
    lines, line_no, position = input.split('\n'), 0, 0
    while position <= offset:
        position += len(lines[line_no]) + 1
        line_no += 1
    message, line = 'Line ' + str(line_no) + ': expected ' + ', '.join(expected) + '\n', lines[line_no - 1]
    message += line + '\n'
    position -= len(line) + 1
    message += ' ' * (offset - position)
    return message + '^'

def parse(input, actions=None, types=None):
    parser = Parser(input, actions, types)
    return parser.parse()
