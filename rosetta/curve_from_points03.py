# curve_from_points03.py
# the add module
# the points module
# "creating geometry from scratch:
# https://wordpress.discretization.de/houdini/home/introduction/creating-geometry-from-scratch/


from __future__ import division, print_function
import hou
import Funs_Lib as fl
reload(fl)
import time


def timestamp():
    'output: timestamp format, ex: 2010.03.12__22.37.0'
    now = time.localtime(time.time())
    # full time tuple, ex: (1998, 9, 26, 10, 56, 59, 5, 269, 1)
    # remove last digit of seconds
    return time.strftime('%Y.%m.%d__%H.%M.%S', now)[:-1]

print()
print("Oskar curve from points: Begin", timestamp())
# print(dir(fl))
print()

# clear Network by loading 'blank' hip file
hou.hipFile.load("M:\Graphics\Houdini\houdini18\CleanCanvas2.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)
geo = hou.node('/obj').createNode('geo')


def create_xform_node(input_node, TR, vector):
    # create transform node with parameters and return node
    node = geo.createNode('xform')
    # set input to node
    node.setInput(0, input_node)
    # set transformation parameter tuple
    node.parmTuple(TR).set(vector)
    return node
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
    point_z = "pt" + str(pointNum) + "z"  # name of point reference coordinate, y
    node.parm(point_x).set(x)         # sets x coordinate, point#: pointNum
    node.parm(point_y).set(y)         # sets y coordinate, point#: pointNum
    node.parm(point_z).set(z)         # sets y coordinate, point#: pointNum
def total_points(node, numpoints):
    node.parm("points").set(numpoints)
    return numpoints
def point_and_sphere(x,y,z):
    set_point(the_points, pointNum, x, y, z)
    # sphere instance node at (x,y,z); xform node
    instance_node = create_xform_node(small_sphere, "t", (x,y,z) )
    # add node to merge node
    Trail.setNextInput(instance_node)


PI = 3.14
STYLE = [ "F", "V", "H", "B" ]   # Function, Vertical, Horizontal, Both


# create merge node; accumulate trail of spheres
Trail = geo.createNode('merge', 'Trail')

# create sphere
the_sphere = geo.createNode('sphere')
# by default at (0,0,0), but not in merge node so invisible
small_sphere = create_xform_node(the_sphere, "s", (0.01, 0.01, 0.01) )


the_points = geo.createNode('add','the_points')
numPoints = total_points(the_points,200)
extent = 1
numSteps = 2
phase = .4

for pointNum in range(numPoints):
    i = pointNum/numPoints
    x = 0
    z = i * extent
    numSteps = 4
    step, j = fl.tremap(numSteps, z)
    y1 = fl.sequence(j, step)
    point_and_sphere(-i, 0, y1)     # x-axis

    step, j = fl.tremap(numSteps, z, .2)
    y2 = fl.sequence(j, step)
    # point_and_sphere(1.0, z , y2)   # -axis

    numSteps = 4
    step, j = fl.tremap(numSteps, z, .15)
    y3 = fl.sequence(j, step)
    point_and_sphere(y3, 0, -i)     # z-axis

    point_and_sphere(y3, .25 , y1)


print
print("Oskar curve from points: Done")
print
print