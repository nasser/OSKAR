import hou
import math

# clear Network by loading 'blank' hip file
hou.hipFile.load("c:/Users/Larry Cuba/untitled.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)

geo = hou.node('/obj').createNode('geo')

# fun(x)::sin(x);
def fun(x):
    return math.sin(x)

# myTY1(x)::.5+(sin(x*360)/2);
def myTY1(x):
    return 0.5 + (math.sin(x*math.pi*2)/2)

# funplot(TY) <<< cube [ {0}
def funplot(TY):
    cube = geo.createNode('box')
    # * ( .02, .02, .5) 
    xform = geo.createNode('xform')
    xform.parmTuple('s').set((0.02, 0.02, 0.5))
    xform.setInput(0, cube)

    # [ {30} + ( i*1.0, TY(i), 0) ] 
    copy = geo.createNode('copy')
    numpix = 30
    copy.parm('ncy').set(numpix)
    copy.parm('cum').set(False)
    # i*1.0
    copy.parm('tx').setExpression("(lvar(\"CY\")/lvar(\"NCY\")) * 1.0", hou.exprLanguage.Python)
    # TY(i)
    hou.expressionGlobals()['TY'] = TY
    copy.parm('ty').setExpression("TY(lvar(\"CY\")/lvar(\"NCY\"))", hou.exprLanguage.Python)
    copy.setInput(0, xform)
    
    # * (1, .5, 1)
    xform2 = geo.createNode('xform')
    xform2.parmTuple('s').set((1.0, 0.5, 1.0))
    xform2.setInput(0, copy)

    return xform2

def curv():
    return funplot(myTY1)

def drawpic():
    c = curv()
    # + (-.5, -.5, 0)
    xform = geo.createNode('xform')
    xform.parmTuple('t').set((-0.5, -0.5, 0.0))
    xform.setInput(0, c)
    # @ ( -30, 0,  0)  # rotate
    xform2 = geo.createNode('xform')
    xform2.parmTuple('r').set((-30, 0.0, 0.0))
    xform2.setInput(0, xform)
    # + ( .5,  .5, 0)
    xform3 = geo.createNode('xform')
    xform3.parmTuple('t').set((0.5, 0.5, 0.0))
    xform3.setInput(0, xform2)

    return xform3

drawpic().setDisplayFlag(1)