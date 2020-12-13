import hou
import math
# clear Network by loading 'blank' hip file
hou.hipFile.load("c:/Users/Larry Cuba/untitled.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)

def fun(x):
    return math.sin(x)

hou.expressionGlobals()['fun'] = fun

geo = hou.node('/obj').createNode('geo')

# slab << cube [ {50}
def slab():
    slab = geo.createNode('box')
    # * ( .02, .02, .5) 
    xform = geo.createNode('xform')
    xform.parmTuple('s').set((0.02, 0.02, 0.5))
    xform.setInput(0, slab)
    # + ( i*1.0, fun(i*360), 0) # move as function(iteration)
    copy = geo.createNode('copy')
    numpix = 150
    copy.parm('ncy').set(numpix)
    copy.parm('cum').set(False)
    copy.parm('tx').setExpression("(lvar(\"CY\")/lvar(\"NCY\")) * 1.0", hou.exprLanguage.Python)
    copy.parm('ty').setExpression("0.5 + fun((lvar(\"CY\")/lvar(\"NCY\")) * (360.0 * (6.283185307179586/360.0))) / 2", hou.exprLanguage.Python)
    copy.setInput(0, xform)
    xform2 = geo.createNode('xform')
    xform2.parmTuple('s').set((0.5, 0.5, 0.5))
    xform2.setInput(0, copy)
    return xform2

# << slab [ {0} 
slab1 = slab()

# + (-1, -.5, 0)
xform1 = geo.createNode('xform')
xform1.parmTuple('t').set((-1, -0.5, 0))
xform1.setInput(0, slab1)
# @ ( -50, 30,  0)
xform2 = geo.createNode('xform')
xform2.parmTuple('r').set((-50, 30, 0))
xform2.setInput(0, xform1)
# * ( 1, .5, 1)
xform3 = geo.createNode('xform')
xform3.parmTuple('s').set((1, 0.5, 1))
xform3.setInput(0, xform2)
# + ( 1,  .5, 0)
xform4 = geo.createNode('xform')
xform4.parmTuple('t').set((1, 0.5, 0))
xform4.setInput(0, xform3)

xform4.setDisplayFlag(1)
