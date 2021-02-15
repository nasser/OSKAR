import hou

def function_name(f):
    """
    compute a unique name for the function f, using its memory address
    to ensure uniqueness. useful when representing closures in expression
    globals.
    """
    return f.__name__ + "_" + hex(id(f))

def global_time():
    """
    compute the top level time of the film, a number from 0.0 to 1.0
    """
    return hou.hscriptExpression("($F-1)/($NFRAMES-1)")

def connect(a, b, index=0):
    """
    connect make node b the input to node a
    """
    a.setInput(index, b)

def export_function(f):
    """
    Make a function f available in the global expression environment as
    function_name(f)
    """
    hou.expressionGlobals()[function_name(f)] = f

def expression_prelude(env_fn):
    """
    generate the prelude code for parameter expressions

    extracts and unpacks a local environment for the parameter from env_fn that
    is expected to return a dictionary with the local variables visible to this
    expression
    """
    export_function(env_fn)
    return ("for name, value in %s().iteritems():\n" % function_name(env_fn) +
            "  exec(name + ' = value')\n" +
            "return ")

def translate(root, name, prelude, x, y, z):
    """
    create a translate transform node, with python expressions for x y and z
    """
    xform = root.createNode('xform')
    xform.parm('tx').setExpression(prelude + x, hou.exprLanguage.Python)
    xform.parm('ty').setExpression(prelude + y, hou.exprLanguage.Python)
    xform.parm('tz').setExpression(prelude + z, hou.exprLanguage.Python)
    xform.setName(name + "_translate")
    return xform

def rotate(root, name, prelude, x, y, z):
    """
    create a rotate transform node, with python expressions for x y and z
    """
    xform = root.createNode('xform')
    xform.parm('rx').setExpression(prelude + x, hou.exprLanguage.Python)
    xform.parm('ry').setExpression(prelude + y, hou.exprLanguage.Python)
    xform.parm('rz').setExpression(prelude + z, hou.exprLanguage.Python)
    xform.setName(name + "_rotate")
    return xform

def scale(root, name, prelude, x, y, z):
    """
    create a scale transform node, with python expressions for x y and z
    """
    xform = root.createNode('xform')
    xform.parm('sx').setExpression(prelude + x, hou.exprLanguage.Python)
    xform.parm('sy').setExpression(prelude + y, hou.exprLanguage.Python)
    xform.parm('sz').setExpression(prelude + z, hou.exprLanguage.Python)
    xform.setName(name + "_scale")
    return xform

def Cube(root, pt):
    """
    create a cube node. takes (and ignores) parent time for compatibility
    with other pictures
    """
    return root.createNode('box')

def iteration_value(path):
    """
    computes the iteration value (from 0.0 to 1.0, generally 'i' in
    oskar code) value for a given houdini for-each node triplet
    identified by path.
    
    the path is expected to be an absolute path to a for-each metadata
    node. this function is only useful inside a parameter expression.
    """
    geo = hou.node(path).geometry()
    return float(geo.attribValue("iteration")) / (geo.attribValue("numiterations") - 1)

def iteration_network(root, name, count):
    begin_name = name + "_begin"
    meta_name = name + "_meta"
    end_name = name + "_end"
    block_begin = root.createNode('block_begin', begin_name)
    block_meta = root.createNode('block_begin', meta_name)
    block_end = root.createNode('block_end', end_name)
    block_begin.parm('blockpath').set('../' + end_name)
    block_meta.parm('blockpath').set('../' + end_name) 
    block_begin.parm('method').set('input')
    block_end.parm('method').set('merge')
    block_meta.parm('method').set('metadata')
    block_end.parm('itermethod').set('count')
    block_end.parm('iterations').set(count)
    block_end.parm('blockpath').set('../' + begin_name)
    block_end.parm('templatepath').set('../' + begin_name)
    block_meta_path = block_meta.path()
    
    connect(block_end, block_begin)
    
    return (block_begin, block_end, block_meta_path)

