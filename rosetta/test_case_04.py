
# test_case_04.py

import hou

# clear Network by loading 'blank' hip file
# hou.hipFile.load("c:/Users/Larry Cuba/untitled.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)

# set viewport view to "Front"
hou.geometryViewportType.Front

 
geo = hou.node('/obj').createNode('geo')

# slab << cube [ {5}
def slab():
    slab = geo.createNode('box')
    # * ( .1, .5, .5) ]
    xform = geo.createNode('xform')
    xform.parmTuple('s').set((0.1, 0.5, 0.5))
    xform.setInput(0, slab)
    # + ( i * 1, 0, 0)
    copy = geo.createNode('copy')
    numpix = 5
    copy.parm('ncy').set(numpix)
    copy.parm('cum').set(False)
    copy.parm('tx').setExpression("(lvar(\"CY\")/lvar(\"NCY\")) * 1", hou.exprLanguage.Python)
    copy.setInput(0, xform)
    return copy

# << slab [ {0} 
slab1 = slab()

# + (-.5, -.5, 0)
xform1 = geo.createNode('xform')
xform1.parmTuple('t').set((-0.5, -0.5, 0))
xform1.setInput(0, slab1)
# @ ( -50, 30,  0)
xform2 = geo.createNode('xform')
xform2.parmTuple('r').set((-50, 30, 0))
xform2.setInput(0, xform1)
# * ( .5, .5, .5)
xform3 = geo.createNode('xform')
xform3.parmTuple('s').set((0.5, 0.5, 0.5))
xform3.setInput(0, xform2)
# + (.5, .5, 0)
xform4 = geo.createNode('xform')
xform4.parmTuple('t').set((0.5, 0.5, 0))
xform4.setInput(0, xform3)

xform4.setDisplayFlag(1)
