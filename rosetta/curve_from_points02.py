# curve_from_points02.py
# the add module
# the points module
# "creating geometry from scratch:
# https://wordpress.discretization.de/houdini/home/introduction/creating-geometry-from-scratch/


from __future__ import division
import hou
import math
import Funs_Lib as fl
reload(fl)
import houdini_calls as hc
reload(hc)

print
print "Oskar curve from points: Begin"

# clear Network by loading 'blank' hip file
hou.hipFile.load("M:\Graphics\Houdini\houdini18\CleanCanvas2.hipnc", suppress_save_prompt=True, ignore_load_warnings=False)
geo = hou.node('/obj').createNode('geo')

PI = 3.14
STYLE = [ "F", "V", "H", "B" ]   # Function, Vertical, Horizontal, Both

# create merge node; accumulate trail of spheres
Trail = geo.createNode('merge', 'Trail')

# create sphere
the_sphere = geo.createNode('sphere')
small_sphere = hc.create_xform_node(geo, the_sphere, "s", (0.01, 0.01, 0.01) )

the_points = geo.createNode('add','the_points')
numPoints = hc.total_points(the_points,180)
extent = 1
numSteps = 4

for pointNum in range(numPoints):
    i = pointNum/numPoints
    x = i * extent
    # y = fl.sin_whole(x)
    # y = fl.rampU(x,fl.curveB, fl.curveF )
    # y = fl.twofer(x, fl.sin_halfF, fl.sin_halfH)
    # y = fl.doubleU(x, fl.upper)
    y = fl.repetitions2(x, numSteps, fl.upper)
    z = 0
    # print(x,y,y1)
    hc.set_point(the_points, pointNum, x, y, z)
    # print(pointNum,(x,y,z))
    # sphere instance node at (x,y,z); xform node
    instance_node = hc.create_xform_node(geo, small_sphere, "t", (x,y,z) )
    # add node to merge node
    Trail.setNextInput(instance_node)



""""

combo's of two functions 
x number of repetitions of a function (or combo's)
horizontal combos and ramp combos; repetition to create larger ramp
and repetition of ramp. 

python has modulo function: divmod

"""




print
print "Oskar curve from points: Done"
print
print