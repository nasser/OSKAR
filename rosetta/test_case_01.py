
# test_case_01.py

import hou

geo = hou.node('/obj').createNode('geo')

# Scene << Cube [ {1} ]
scene = geo.createNode('box')

scene.setDisplayFlag(1)