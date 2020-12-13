#
# houdini_calls.py
#
# functions specific to houdini #

def total_points(node, numpoints):
    node.parm("points").set(numpoints)
    return numpoints

def set_point(node, pointNum, x, y, z):
    # houdini calls to create point and set coords
    pointName = "usept" + str(pointNum)
    node.parm(pointName).set(1)          # displays point
    point_x = "pt" + str(pointNum) + "x"  # name of point reference coordinate, x
    point_y = "pt" + str(pointNum) + "y"  # name of point reference coordinate, y
    node.parm(point_x).set(x)         # sets x coordinate, point#: pointNum
    node.parm(point_y).set(y)         # sets y coordinate, point#: pointNum


def create_xform_node(geo, input_node, TR, vector):
    # create transform node with parameters and return node
    node = geo.createNode('xform')
    # set input to node
    node.setInput(0, input_node)
    # set transformation parameter tuple
    node.parmTuple(TR).set(vector)
    return node

def add_xform_node(geo, array, picNum, xform_num, TR, vector):
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




