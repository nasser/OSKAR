"""
This file specifies a generator that takes output from the OSKAR compiler
and converts it into runnable OpenSCAD code.

This file was written by Bryce Summers for Larry Cuba on:
1 - 22 - 2017.

This file was inspired by a similar one written by Larry.

If the interface is maintained, this generator may easily be substituted for one that targets a language other than OpenSCAD.
For instance, OpenGL or WebGl could be targeted.
"""
from datetime import datetime
import pdb # Debugger.


class Scene:

    def __init__(self):
        self.filePath = ".\\"
        self.fileName = self.filePath + "\\output.scad"


        # FIXME: Please renamed these to objects, instead of pictures.
        # These data structures represent all of the generation objects.

        self.pictures = [] # List of Pictures, each of which specifies an OpenSCAD module.
        self.current_picture = None # The current object that this generator is specifying.


    def newPicture(self, name):

        self.finishLastPicture()
        self.current_picture = Picture(name)
        self.current_picture.make_normal_picture()
        self.pictures.append(self.current_picture)

    def newDirectPicture(self, name):

        self.finishLastPicture()
        self.current_picture = Picture(name)
        self.current_picture.make_direct_picture()
        self.pictures.append(self.current_picture)


    def newDrawCommand(self, name):

        self.finishLastPicture()
        self.current_picture = Picture(name)
        self.current_picture.make_draw_command()
        self.pictures.append(self.current_picture)

    def newFunction(self, name):
        self.finishLastPicture()
        self.current_picture = Function(name)
        self.pictures.append(self.current_picture)
        return self.current_picture



    """
    Currently we implement picture generation by routing all
    of these calls to the latest picture.
    """
    def addArgument(self, arg):
        self.current_picture.addArgument(arg)

    # string, int, int
    # for(int var = begin; var < end; var++)
    def iterations(self, var, begin, end):
        self.current_picture.iterations(var, begin, end)


    # string, string, string
    def scaling(self, sx, sy, sz):
        self.current_picture.scaling(sx, sy, sz)


    def translation(self, tx, ty, tz):
        self.current_picture.translation(tx, ty, tz)


    def rotation(self, rx, ry, rz):
        self.current_picture.rotation(rx, ry, rz)


    def basis(self, name):
        self.current_picture.basis(name)

    def addBasisArgument(self, name):
        self.current_picture.addBasisArgument(name)


    def color(self, r, g, b, a):
        self.current_picture.color(r, g, b, a)

    def expression(self, txt):
        self.current_picture.expression(txt)

    def anonymous(self, isAnonymous):
        self.current_picture.anonymous(isAnonymous)


    # Complete the definition for the last picture that was defined.
    def finishLastPicture(self):
        if self.current_picture is not None:

            # Since the current OSKAR specification does not
            # mention colors, we specify defaault grey colors
            # here.
            self.current_picture.finish()


    def generateCode(self):
        self.finishLastPicture()

        # List of Strings representing lines of code.
        output = []
        self.generateHeader(output)

        macrosubber = MacroSubstitutor()

        # Generate all definitions and macrosubstitute functional arguments as needed.
        # definitions include picture definitions, functions, direct functions, draw commands, etc.
        for x in range(len(self.pictures)):

            definition = self.pictures[x]
            substitutionText = definition.getSubstitutionText()
            macrosubber.addSubstitutionText(substitutionText)

        # Generate all of the code at the end.
        output.append(macrosubber.generateCode())

        # Append the final draw Command.
        last_picture = self.pictures[len(self.pictures) - 1]
        name = last_picture.getName()
        output.append("// Draw the root module.")
        # output.append("translate([0, 0, 0])rotate([-58,-20, -15]) //set POV")
        output.append(name + "();")


        # Join the list of strings with a newLine character.
        fileText = "\n".join(output)

        self.sendToFile(self.fileName, fileText)


    # Appends a list of strings to the given String[] output object.
    def generateHeader(self, output):

        output.append("//  OpenScad code generated from OSKAR python.")
        output.append("//  OSKAR Compiler written by Bryce Summers for Larry Cuba")
        output.append("//  Compiled on "+ "{:%B %d, %Y}".format(datetime.now()))
        output.append("$fn=130;")
        output.append("$vpr = [0, 0, 0];   // vpr system variable")
        output.append("$vpd = 3.0;         // vpd system variable")
        output.append("$vpt = [1., 0.55, 0];   // vpt system variable")
        output.append("\n")

        output.append("\n".join(
            ["function modulo(dividend, divisor) =",
             "   dividend % divisor;",
             "",
             "// return 0, divisor, 2*divisor, etc based on which interval x is in.",
             "function step(x, divisor) = ",
             "    floor(x/divisor)*divisor;",
             ""]))


    def sendToFile(self, fileName, fileText):
        file = open(fileName,"w")
        file.write(fileText)
        file.close()

# Pictures gradually build their OpenScad text as they are called through a genaricized interface.
class Picture:

    def __init__(self, name_in):
        self.text = []
        self.myName = name_in

        self.name_created = False

        # Name is set later, when we have the full list of arguments.
        #self.name(name_in)

        self.arguments = []

        self.basisArguments = []

        # We keep a list of transforms, because OpenSCAD insists on
        # having their transforms specified in funky reverse order.
        self.transforms = []

        # 3 space and 6 space indents.
        self.indent1 = "   "
        self.indent2 = self.indent1*2

        self.isDrawCommand   = False
        self.isNormalPicture = False
        self.isDirectPicture = False # Picture Reduction.
        self.isAnonymous   = False

    def make_normal_picture(self):
        self.isNormalPicture = True

    def make_draw_command(self):
        self.isDrawCommand = True

    def make_direct_picture(self):
        self.isDirectPicture = True

    def name(self, name, arguments):

        str = "module " + name + "("

        for i in range(len(arguments) - 1):
            str += arguments[i] + ", "
        if len(arguments) > 0:
            str += arguments[len(arguments) - 1]
        str += ")"

        self.text.append(str)
        self.text.append("{")

        # this might not be the best place for this
        # but it ensures that Global_t is defined in
        # each module --nasser
        self.text.append(self.indent1 + "Global_t = $t;")

    # add an arugment name.
    def addArgument(self, arg):
        self.arguments.append(arg)

    def getName(self):
        return self.myName

    # string, int, int
    # for(int var = begin; var < end; var++)
    def iterations(self, var, begin, end):

        self.name(self.myName, self.arguments)

        # Openscad does not support programmatic time specification.
        if self.isDrawCommand:
            return

        # Assuming we always go from 0 to 1 with end steps...
        #step = 1.0 / end # As of 5.15.17, we no longer do this and we use strings now.

        #self.text.append(self.indent1 + "begin = 0;")
        self.text.append(self.indent1 + "steps = " + str(end) + ";")
        self.text.append(self.indent1 + "step_size = 1.0/steps;")
        #self.text.append(self.indent1 + "end   = 1;")
        self.text.append(self.indent1 + "// Iteration from 0 to 1 in " + str(end) + " equal steps.")
        self.text.append(self.indent1 + "for (" + var + "=[0:step_size:1])")
        self.text.append(self.indent1 + "{")

    def expression(self, txt):
        # Create the header if it doesn't yet exist.
        if not self.name_created:
            self.name(self.myName, self.arguments)
        self.text.append(self.indent1 + txt + ";")

    # string, string, string
    def scaling(self, sx, sy, sz):
        self.transforms.append(self.indent2 + "scale([" + sx + ", " + sy + ", " + sz + "])")


    def translation(self, tx, ty, tz):
        self.transforms.append(self.indent2 + "translate([" + tx + ", " + ty + ", " + tz + "])")

    def rotation(self, rx, ry, rz):
        self.transforms.append(self.indent2 + "rotate([" + rx + ", " + ry + ", " + rz + "])")

    def color(self, r, g, b, a):

        # Avoid cluttering the draw commands.
        if self.isDrawCommand:
            return

        self.text.append(self.indent2 + "color([" + r + ", " + g + ", " + b + ", " + a + "])")

    def addBasisArgument(self, name):
        self.basisArguments.append(name)

    def basis(self, name):
        self._reversePushTransforms()
        self.color("1", "1", "1", "1")
        if self.isAnonymous:
            self.text.append(self.indent2 + name + "(" + ",".join(self.arguments) + ");")
        elif len(self.basisArguments) != 0:
            self.text.append(self.indent2 + name + "(" + ",".join(self.basisArguments) + ");")
        else:
            self.text.append(self.indent2 + name + "();")

    def anonymous(self, isAnonymous):
        self.isAnonymous = isAnonymous

    # Here we reverse the order of the transforms from the original C*B*A*[] order,
    # which is the order that a person would left multiply matrices.
    # to the funky reverse ordering of OpenSCAD.
    def _reversePushTransforms(self):
        while len(self.transforms) > 0:
            self.text.append(self.transforms.pop())

    def finish(self):
        # Closing brace for end of iteration loop in normal picture definitions.
        if self.isNormalPicture:
            self.text.append(self.indent1 + "}")
        self.text.append("}\n")

    # Returns a string representing the OpenSCAD code for
    # this picture definition.
    def generateCode(self, output):
        output += self.text

    def getSubstitutionText(self):
        return SubstitutableText(self.myName, self.arguments, "\n".join(self.text))


class Function:

    def __init__(self, name_in):
        self.myName = name_in

        self.args = []        # Strin[]
                              # A list of argument variable names.
        self.expressions = [] # String[]
                              # A list of evaluation expressions for every dimension.

        self.scalar = False   # This stores whether this is a scalar function.
        self.vector = False   # This stores whether this is a vector function.

        self.transforms = []

    # Return Types of functions.
    def scalar_type(self):
        self.scalar = True

    def vector_type(self):
        self.vector = True

    # Names of inputs variables.
    # String[] -> ()
    def addArgument(self, arg):
        self.args.append(arg)

    # String ->
    def addExpression(self, exp):
        self.expressions.append(exp)

    # Finishes this object.
    def finish(self):
        return

    # Returns a string representing the OpenSCAD code for
    # this picture definition.
    # ASSUMPTION: finish() has been called to finish this picture.
    def generateCode(self, output):

        # Code String, complete with line breaks.
        out = ""

        # 3 space and 6 space indents.
        self.indent1 = "   "
        self.indent2 = self.indent1*2


        # Header.
        out += "function "

        # function name
        out += self.myName + "("

        # Arguments.
        for i in range(0, len(self.args) - 1):
            out += self.args[i] + ", "
        out += self.args[len(self.args) - 1]
        out += ") = \n"

        out += self.indent1

        # If this is a scalar function, then we are done.
        if(self.scalar):
            out += self.expressions[0] + ";\n\n"
            output.append(out)
            return

        if(self.vector):
            # Vector functions.
            out += "["
            for i in range (0, len(self.expressions) - 1):
                out += self.expressions[i] + ", "
            out += self.expressions[len(self.expressions) - 1]
            out += "];\n"

            output.append(out)
            return

    def getSubstitutionText(self):
        body = []
        self.generateCode(body)
        body_text = "\n".join(body)
        return SubstitutableText(self.myName, self.args, body_text)


"""
Macrosubstitution code.
Written by Bryce Summers beginning on May.15.2017

This code is necessary for getting around Open Scad's non-support for 1st class functions.
Instead of directly passing function arguments, I've created macrosubstituted version of every function with
every set of funcion called values directly inserted into the code.
"""

class SubstitutableText:

    # String, String[], String.
    # name of function,
    # names of local variables passed into the function.
    # Textual body that makes up the original function in a file.
    # If a language allows 1st class functions, the body would be the final
    # form of the function.
    # In languages without 1st class functions, like Openscad,
    # we will perform macrosubstitution on this body.
    def __init__(self, name, arguments, body):
        self.myName = name
        self.myArgs = arguments
        self.myText = body

    def __repr__(self):
        return "Name: " + self.myName + "\n" + "Arguments: " + self.myArgs.__repr__() + "\n" + self.myText

    def getName(self):
        return self.myName

    # Returns the argument variable names, ignoring the default values.
    def getArgs(self):

        output = []
        for argument in self.myArgs:
            output.append(argument.split('=')[0])

        return output

    # Used at the end to retrieve the body, which may be written out to a file.
    def getBody(self):
        return self.myText


    # Returns a Substitutable text object equivalent to
    # replacing the body substituting
    # the find string for the replace string.
    # The inputs are two index associated lists that
    # allow for several macrosubstitutions to be done at once.
    # set(int), String[]
    def macroSubstitute(self, find_indices_set, replaces):

        # Translation from int[], String[] form to
        # direct String --> String form.
        old_args = self.getArgs()
        finds = []

        for arg_index in find_indices_set:
            arg = old_args[arg_index]
            finds.append(arg)

        # The name is constructed by adding the macrosubstituted argument underscored in.
        old_name = self.getName()
        new_name = old_name
        for str in replaces:
            new_name = new_name + "_" + str

        # Construct the argument list, minus the arguments that are to be
        # directly macrosubstituted into the text.
        new_args = []
        finds_set = set(finds)
        for arg in old_args:
            if (arg not in finds_set):
                new_args.append(arg)

        # Create the new body by replacing all instances of find with replace.
        new_body = self.getBody()
        for index in range(len(finds)):
            find_str    = finds[index]
            replace_str = replaces[index]
            new_body    = new_body.replace(find_str, replace_str)


        output_func = SubstitutableText(new_name, new_args, new_body)

        # Update the body with the correct new name and filtered argument list.
        header_leftP = new_body.find(old_name) + len(old_name)
        output_func.removeArgumentCalls(find_indices_set, header_leftP)

        return output_func

    # Finds the

    # if the function is passed as a function reference

    # returns the index of the '('.
    # returns -1 if not found.
    def isInsideOtherSubtext(self, other):

        str = other.getBody()

        # Returns True if the name is found, it is followed by a '('
        # and preceded by a space or the beginning of string.
        name_index = str.find(self.myName)
        name_found = (name_index > -1)

        if not name_found:
            return -1

        # end index is inferred by the search string.
        end_index = name_index + len(self.myName)
        endP_index = end_index

        # These criteria are used to find a call to self.myName() inside
        # the body of the other.
        followed_by_leftp = (str[endP_index] == '(')
        preceded_by_space = name_index == 0 or str[name_index - 1] == ' ' or str[name_index - 1] == '\n'
        if name_found and followed_by_leftp and preceded_by_space:
            return endP_index

        # function name not found.
        return -1

    # Takes self's body changes the function names to name_called_function.
    # modifies self.body by taking the function call located at leftP_index
    # INPUT: set(ints), int
    # 1. Cuts the body at parentheses.
    # 2. finds names of arguments at indices.
    # 3. appends arguments to name before cut.
    # 4. adds the arguments not in the find indices. (are they sorted or a set?)
    # 5. Stitches the bodies back together.'
    # ENSURES: Returns this substitution text, only it has a modified body.
    # WARNING: This function modifies self object.
    def removeArgumentCalls(self, find_indices_set, leftP_index):

        # Step 1: Determine the length of '(' through ')'

        # TODO: Write this function.
        rightP_index = self.searchForRightP(self.myText, '(', ')', leftP_index)


        # Step 2: split self.myText into prefix, '('args')', postfix.
        prefix_str  = self.myText[:leftP_index]
        arg_str     = self.myText[leftP_index:rightP_index + 1]
        postfix_str = self.myText[rightP_index + 1:]


        # Step 3: Split the args up into a list of names.
        arg_list = self.splitPList(arg_str, '(', ')', ',')


        # Step 4: Remove all function names from the list.
        # Step 5: Concatenate the prefix to the args list to the postfix list.
        filtered_arg_list = []
        for x in range(len(arg_list)):
            argument = arg_list[x]

            # Step 5. create a unique name for modified function.
            if x in find_indices_set:
                prefix_str += "_" + argument.split('=')[0] # Ignore and default parameters.
            # Step 4. form the filtered list.
            else:
                filtered_arg_list.append(argument)

        # Step 6: Reconcatenate the args list.
        arg_str = "("
        for argument in filtered_arg_list[:-1]:
            arg_str += argument + ", "

        # Add the last argument if any.
        length = len(filtered_arg_list)
        if length > 0:
            arg_str += filtered_arg_list[length - 1]

        # Finish it off with a right parens.
        arg_str = arg_str + ")"


        # Step 7: Form the name, arglist, and body for the modified substitution text.
        self.myText = prefix_str + arg_str + postfix_str

        return self


    # Return the index of the right parentheses associated with the given left parentheses.
    # Returns -1 if rightP not found.
    # String, char, char, int
    def searchForRightP(self, text, leftP, rightP, leftP_index):

        scope = 1
        index = leftP_index
        length = len(text)

        while(scope > 0):

            # Proceed to the next character.
            index += 1

            # End of file found.
            if index > length:
                return -1

            char = text[index]

            if char == leftP:
                scope += 1
            elif char == rightP:
                scope -= 1

            continue

        return index

    # Input: "(a, (b+c) , d)" -> '(' -> ')' -> ',' --> ["a", "(b+c)", "d"]
    # String, char, char, char
    def splitPList(self, text, leftP, rightP, separator):

        # ASSUMPTION: text[0] == '('
        # ASSUMPTION: arguments will not have spaces in them.

        scope = 1 # We begin within 1 left parens.
        scanning = False
        index = 0 # The current index.
        scan_start_index = 0 # The index where the element scan began.
        length = len(text)

        output = []

        # Can through the text once.
        while(index < length - 1):
            index += 1

            char = text[index]

            # End of scan. Note: the scan can only end within the original scope.
            if scope == 1 and (char == ',' or char == ' ' or char == ')') and scanning:
                output.append(text[scan_start_index:index])
                scanning = False

            # Beginning of scan. Can't happen when a scan has ended.
            elif not scanning and char != '_':
                scanning = True
                scan_start_index = index


            # Modify the scope.

            # Decrease scope.
            if char == rightP:
                scope -= 1
            # Handle parens scope.
            elif char == leftP:
                scope += 1

        return output

class MacroSubstitutor:

    def __init__(self):

        self.functions = []
        self.func_name_set = set()

    def generateCode(self):
        output = ""
        for func in self.functions:
            output = output + func.getBody()

        return output

    # Using a Trampoline, macrosubstitute all function calls
    # down the entire necessary call chain.
    def addSubstitutionText(self, subText):
        subbed_funcs = [subText]

        # Trampoline.
        while(len(subbed_funcs) > 0):

            # 1. func come in.
            func = subbed_funcs.pop()

            # If the function has been previously defined, we ignore it.
            if func.getName() in self.func_name_set:
                print("WARNING: The function named \"" + func.getName() + "\" has previously been defined already, so the python generator is skipping all but the first definition.")
                continue

            # 2. func is modified and may produce some new funcs.
            new_funcs = self.addSubstitutionText_helper(func)

            # 3. We log the modified func into our data structures and it may be substituted
            # by future calls.
            # Add new functions as they come along.
            if func.getName() not in self.func_name_set:
                print(func.getName())
                print(self.func_name_set)
                self.functions.append(func)
                self.func_name_set.add(func.getName())

            # 4. add the newly produced funcs to the queue, because they may need to be modified.
            for new_func in new_funcs:
                subbed_funcs.append(new_func)


    # Called every time a new function is created.
    # INPUT: The calling function that may call a pre-existing function with a function argument.
    # Here are some naming conventions to try to keep the functions straight.
    # bryce() <-- definition
    # bar()   <-- definition
    # foo()   <-- definition
    # {
    #  bar(   <-- function call.
    #      bryce, <-- function reference.
    #     )
    # }
    #
    # INPUT: new_def, a new function definition that may have calls to pre-existing definitions that take function references.
    # new_def is a SubstitutionText object.
    #
    # We map the local variables defined in the pre-existing function's
    # function signature to the names of pre-existing functions that would have been
    # passed in for a language that supports function passing.
    # then may then omit those entries from the function signature, because they
    # have been implicitly passed through via the hard coded substitution.
    #
    # FIXME: I've noticed that my language is very imprescise in this function, it would clarify my thinking if I had better language.
    #
    # For Example:
    # func:  g(f, x) = f(x)  <-- Pre-existing function.
    #
    # h: h(x) = x + 2        <-- Pre-existing function.
    # subText: foo = g(h, 5) <-- function that is to be macrosubstituted.
    #
    # Generated Macrosubstituted function:
    # g_h(x) = h(x)
    # Altered definition of foo:
    # foo = g_h(5)
    #
    def addSubstitutionText_helper(self, new_def):

        subbed_funcs = []

        # Consider every pre-existing function definition.
        for func in self.functions:


            #if new_def.getName() == "wallpaper":
            #    pdb.set_trace()

            # We iterate through all function calls to func in new_def.
            while True:

                # To do so, we only need to find the first call,
                # because we will replace every function that matters with a new name as we perform substitutions.
                # leftP_index is the index in the subText's new_def's body of parentheses at the start of the arguments of the function call.
                leftP_index = func.isInsideOtherSubtext(new_def)

                # new_def no longer makes any calls to func.
                if leftP_index < 0:
                    break


                # Determine whether or not the call to func contains a function reference argument.
                # To do so we list all of the arguments and see if one of them is the name of a previously defined function.
                # While we are doing so, we keep a record of all of the function arguments found.
                arguments = self.parseArguments(new_def.getBody(), leftP_index)

                # Array of indices of arguments in the function call
                finds    = [] # int[]

                # Array of names of pre-existing functions that are to be substituted for the local variables denoted by the finds.
                replaces = [] # String[]

                # We need the indices, because we know the replaced value in the calling function, but not
                # the local variable in the called function. The index will be invariant and is useful for Substitution text internal functions.
                # We'll need to look up an array of the arguments in the called function
                # or pass indices to the SubstitutableText objects.

                # Search the argument names in the calling function.
                for arg_index in range(len(arguments)):

                    var_name = arguments[arg_index]
                    # For every argument that is the name of a pre-existing function,
                    # we will wish to replace the cooresponding argument at that index in the called function
                    # with the pre-existing function name.
                    if var_name in self.func_name_set:
                        replaces.append(var_name)
                        finds.append(arg_index)

                # The called function does not take function references, of they are not yet defined.
                if len(finds) < 1:
                    break

                # For the given previously defined function, take the arguments
                # at the indices specified in finds and hard substitutes it for
                # the strings in the replaces list.
                # FIXME: macrosubstituted function needs to strip its body' header.
                subbed_func = self.macrosubstitute(func, finds, replaces)
                subbed_funcs.append(subbed_func)

                # To avoid reprocessing the same function call,
                # we change its call to the newly_created macroreplaced definition and take away all of its function arguments.
                new_def = new_def.removeArgumentCalls(finds, leftP_index)

        # The newly created function definitions created via macroreplacement from original definitions will now be added to the file,
        # while also having its function reference containing function calls replaced like new_def's were.
        # To avoid stack overflow they are handled in the addSubstitutionText() function that Trampolines using this helper function.
        return subbed_funcs


    # String, Integer --> returns a list of argument names.
    # Text to be parsed, index of original left parens.
    # ignore default arguments like in the signature foo(base=cube) --> base
    def parseArguments(self, body, leftP_index):
        output = []
        # Parse from '(' to ')', then separate arguments by ',' after removing ' ' spaces.
        in_count = 1

        # Index of first character after the first '('
        index = leftP_index
        arg_start_index = index + 1
        scanning = True
        while(in_count > 0):
            index += 1

            char = body[index]
            if char == '(':
                in_count += 1
                continue
            elif char == ')':
                in_count -= 1

            if char == ',' or char == ')' or char == '=':
                # [inclusive, exclusive)

                # Add the argument if we were scanning.
                # Don't add the argument if it is something like a default argument.
                if scanning:
                    arg_str = body[arg_start_index:index]
                    output.append(arg_str.strip())

                # In any event, move on to the next argument.
                arg_start_index = index + 1

                # Start scanning for the next argument after a comma,
                # but stop scanning after things like an '=' which indicate a default argument afterwards.
                scanning = char == ','

        return output


    # SubstitutionText Object, int[], String[]
    # the initial object that is to be mapped to a substitution,
    # finds: an array denoting the indices of local arguments that are to be substituted by the
    # cooresponding strings in the replaces array.

    # function naming is name_1stPassedFuncName_2ndPassedFuncName_3rdPassedFuncName_etc
    # This will be consistent across macrosubstitution calls, because of the determined
    # order of arguments. If the same functions are passed as arguments to the same
    # macrosubstitution functor, then they will produce the same named macrosubstituted function,
    # which means that we might want to store a set of all names, to avoid naming conflicts
    # and route identical functor evaluations to the same strings to avoid combinatorial explosion.
    # We also might need to worry about user inputs of names like foo_bar, if there is also
    # a function called foo, where the user passes in bar.
    def macrosubstitute(self, func, find_indices, replaces):

        subbed_function = func.macroSubstitute(find_indices, replaces)
        return subbed_function


    # Testing functions.
    def unit_tests(self):
        str = 'foo(a, bb, ccc, dd, e)'

        args = self.parseArguments(str, 3)

        assert(len(args) == 5)
        assert(args[0] == "a")
        assert(args[1] == "bb")
        assert(args[2] == "ccc")
        assert(args[3] == "dd")
        assert(args[4] == "e")

# New operator is implied.
macro = MacroSubstitutor()
macro.unit_tests()
