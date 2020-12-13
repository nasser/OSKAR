# curve_from_points01.py
# the add module
# the points module
# "creating geometry from scratch:
# https://wordpress.discretization.de/houdini/home/introduction/creating-geometry-from-scratch/
#


from __future__ import division
import hou
import math

print
print "Oskar curve from points: Begin"


# clear Network by loading 'blank' hip file
hou.hipFile.load("M:\Graphics\Houdini\houdini18\CleanCanvas3.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)
geo = hou.node('/obj').createNode('geo')

def add_xform_node(array, picNum, xform_num, TR, vector):
    """

    creates a new transformation node, sets its parameters; links to previous node

    array - identifier; name of array of nodes
    index - integer; iteration index, picNum in numPix loop
    xform_num - integer; transformation number in list of xforms
    TR -    character; which transformation? codes: "s", "r", or "t"
    vector - tuple; parameters for transformation (TRx, TRy, TRz );
    """
    # create transform node and add to array of nodes
    nodeName = "xform_" + str(picNum) + "-" + str(xform_num)
    array[picNum].append(geo.createNode('xform', nodeName))
    # set input to previous node: (transform_number - 1)
    array[picNum][xform_num].setInput(0, array[picNum][xform_num - 1])
    # set transformation parameter tuple
    array[picNum][xform_num].parmTuple(TR).set(vector)

def set_point(node, pointNum, x, y, z):
    # houdini calls to create point and set coords
    pointName = "usept" + str(pointNum)
    node.parm(pointName).set(1)          # displays point
    point_x = "pt" + str(pointNum) + "x"  # name of point reference coordinate, x
    point_y = "pt" + str(pointNum) + "y"  # name of point reference coordinate, y
    node.parm(point_x).set(x)         # sets x coordinate, point#: pointNum
    node.parm(point_y).set(y)         # sets y coordinate, point#: pointNum

PI = 3.14

final = geo.createNode('merge', 'final')
first = geo.createNode('add','first')
numPoints = 50
extent = 1
first.parm("points").set(numPoints)        # sets number of points

for pointNum in range(numPoints):
    i = pointNum/numPoints
    x = i * extent
    y = (math.sin(i * PI/1.2)/2)+.5
    z = 0
    set_point(first, pointNum, x, y, z)

final.setNextInput(first)

second = geo.createNode('add','second')
numPoints = 50
extent = 1
second.parm("points").set(numPoints)        # sets number of points

for pointNum in range(numPoints):
    i = pointNum/numPoints
    x = -(i * extent) + 2.
    y = (math.sin(i * PI/1.2))
    z = 0
    set_point(second, pointNum, x, y, z)

final.setNextInput(second)


# make a sphere
# add a copy to points node
# set inputs to first, sphere


# usept0;  pt0x, pt0y, pt0z




"""
# create merge node; add inputs at end of loop;
# "Row" is picture name; "Cube" is basis picture
Row = geo.createNode('merge', 'Row')
numCubes = 7
numRows = 5

Nodes = []                      # set up copies_of_basis array

# BEGIN PICTURE ITERATION LOOP
for rowNum in range(numRows):
    print
    j = rowNum / numRows
    print "Row, j  ", rowNum, j

    # BEGIN PICTURE ITERATION LOOP
    for CubeNum in range(numCubes): # CubeNum = 0 to (numCubes - 1)
        Nodes.append([])            # set up transforms array;
        xfnum = -1                  # to start at 0 after 1st increment

        i = CubeNum/numCubes
        con = (rowNum * numCubes) + CubeNum
        print "cubenum", CubeNum, "con", con, "  ",
        # create Basis (cube) copy number con, (xform # 0)
        boxname = "BOX_" + str(con) + "-0"
        Nodes[con].append(geo.createNode('box',boxname))
        # put Box at Center_Screen

        xfnum += 1; Nodes[con][xfnum].parmTuple("t").set((0.5, 0.5, 0.5))
        # a call to an add_xform_node function would create a new node;
        # instead this just updates transforms builtin to box node

        # TRANSFORMS:

        #   +(-0.5, -0.5, -0.5) ;move to origin
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 't', (-0.5, -0.5, -0.5))

        #   *( .1, .5, .5)     ;scale to slab
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 's', (0.05, 0.2, 0.2))

        #   @( -50, 30,  0)     ;rotate
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 'r', (-50, 30, 0))

        #   *( .5, .5, .5)      ;scale down
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 's', (0.5, 0.5, 0.5))

        #   +(-.4+(i*1.), 0, 0)   #(move as f(i)
        ry = (con * 3.0)    # rotate as f(con)
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 'r', (0, ry, 0))


        #   position in grid using j and i
        ty = -.4 + (j * 1.0)     #   1.0 is extent of array
        tx = -.4 + (i * 1.0)     #   1.0 is extent of array
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 't', (tx, ty, 0))

        #   +(.5, .5, .5)   #(move back to center screen)
        xfnum += 1; add_xform_node(Nodes, con, xfnum, 't', (0.5, 0.5, 0.5))

        #  current node is Nodes[i][xfnum]
        #  last transform in list is input of merge node, 'Row'
        print CubeNum, con,xfnum,"cube,con,xfnum"
        Row.setNextInput(Nodes[con][xfnum])

# After picture iterations loop:
Row.setDisplayFlag(1)                     # set display flag of 'Row', the merge node
"""



print
print "Oskar curve from points: Done"
print
print