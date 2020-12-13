
# test_case_03.py


import hou

geo = hou.node('/obj').createNode('geo')

# slab << cube [ {0} * ( .1, .5, .5) ]
def slab():
    slab = geo.createNode('box')
    xform = geo.createNode('xform')
    xform.parmTuple('s').set((0.1, 0.5, 0.5))
    xform.setInput(0, slab)
    return xform

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
