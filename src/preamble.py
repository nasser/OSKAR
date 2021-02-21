import math
import hou

class Thunk:
    def __init__(self, f):
        self.f = f
    
    def __call__(self):
        return self.f()

def sin(x):
    """
    sin function that operates on degrees
    """
    return math.sin(x * (math.pi/180))

def cos(x):
    """
    cos function that operates on degrees
    """
    return math.cos(x * (math.pi/180))

def function_name(f):
    """
    compute a unique name for the function f, using its memory address
    to ensure uniqueness. useful when representing closures in expression
    globals.
    """
    return f.__name__ + "__" + hex(id(f))

def export_function(f):
    """
    Make a function f available in the global expression environment as
    function_name(f). Returns the global function name of f.
    """
    name = function_name(f)
    hou.expressionGlobals()[name] = f
    return name

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

def Cube(root, pt):
    """
    create a cube node centered at (.5,.5,.5). takes (and ignores) parent time
    for compatibility with other pictures
    """
    cube = root.createNode('box')
    cube.parmTuple('t').set((.5,.5,.5))
    return cube

def Sphere(root, pt):
    """
    create a sphere node centered at (.5,.5,.5). takes (and ignores) parent time
    for compatibility with other pictures
    """
    sphere = root.createNode('sphere')
    sphere.parmTuple('rad').set((.5,.5,.5))
    sphere.parmTuple('t').set((.5,.5,.5))
    sphere.parm('type').set("poly")
    return sphere

def Cylinder(root, pt):
    """
    create a cylinder node centered at (.5,.5,.5). takes (and ignores) parent time
    for compatibility with other pictures
    """
    cylinder = root.createNode('tube')
    cylinder.parmTuple('rad').set((.5,.5))
    cylinder.parmTuple('t').set((.5,.5,.5))
    return cylinder

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

def create_boolean(root, lhs, rhs, op):
    boolean = root.createNode('boolean')
    boolean.parm('booleanop').set(op)
    connect(boolean, lhs, 0)
    connect(boolean, rhs, 1)
    return boolean

_name_count = {}
def unique(s):
    if s in _name_count:
        _name_count[s] += 1
        return "%s_%d" % (s, _name_count[s])
    else:
        _name_count[s] = 0
        return s

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