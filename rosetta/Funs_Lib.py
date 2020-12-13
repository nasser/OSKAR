#
# Funs_Lib  -  Function Library
#

import math

print "funs_lib imported"
# print(dir())
PI = 3.14

def remap(numsteps, i):
    # returns tuple: (current step# , new_i within that step)
    segLength = 1./numsteps
    tuple = (int(i/segLength), numsteps * (i % segLength) )
    return tuple
def sine(x):
    # sin() function height normalized: 0-1
    return (math.sin(x)/2) + .5
def mirror(function):                               # (0,F), (1,V) (2,H) (3,B)
    def wrapper(x, style="F", *args, **kwargs):         # def wrapper(x, style="V", *args, **kwargs):
        if (style == "H") or (style == "B"): x = 1-x    # H or B
        z = function(x, style, *args, **kwargs)           # z = function(x, style, *args, **kwargs)   # F
        if (style == "V") or (style == "B"): z = 1-z    # V or B
        return z
    return wrapper

def mirrorV(function):                               # (0,F), (1,V) (2,H) (3,B)
    def wrapper(x):         # def wrapper(x)
        x = 1-x             #  Vertical Reflection
        z = function(x)     #  call function
        return z
    return wrapper

@mirrorV
def curve(x):
    a = (x * PI / 2);
    y = math.sin(a)
    return y

def curveF(x):
    a = (x * PI / 2);
    y = math.sin(a)
    return y

def curveV(x):
    a = ((1-x) * PI / 2);
    y = math.sin(a)
    return y

def curveH(x):
    a = (x * PI / 2);
    y = 1 - math.sin(a)
    return y

def curveB(x):
    a = ((1-x) * PI / 2);
    y = 1 - math.sin(a)
    return y

def line():         # line primitive - horizontal up, down; angle ramp up, down
    y = 0                # i (bet 0,1) is percentage; don't need to know numPoints
                            # a and b are coordinates (vectors or lists?)
                            # then vector math interpolates x,y,z between a, b, at 'i' percent

def combo(x, fun_a, fun_b, style="V"):   # a 'combo' is two functions, a,b, combined. steps = 2
    step, j = remap(2, x)               # x is position in combo between 0,1
    if step == 0:
        y = fun_a(j, style = "F")
    else:
        y = fun_b(j, style = "V")
    return y
def tremap(numsteps, i, phase = 0):
    # returns tuple: (current step# , new_i within that step)
    i = i + phase
    # i = wrap(i)             #  wraparound to 0 - 1 range
    segLength = 1./numsteps
    tuple = (int(i/segLength), numsteps * (i % segLength) )
    return tuple

def wrap(i):
    # takes a number between 0 and 2; wraps around anything over 1.0
    step, j = divmod(i,1)
    return j

def twofer(x, a, b):
    # two functions, a,b, combined. steps = 2
    step, j = remap(2, x)      # step is either 0 or 1
    if step: y = b(j)     # step is 1, ergo function b
    else: y = a(j)        # step is 0, ergo function a
    return y
def rampD(x, a, b):      # Ramp Down
    # two functions, a,b, combined. steps = 2
    step, j = remap(2, x)    # step is either 0 or 1
    if step:                 # step is 1, ergo function b
        return .5 * b(j)     # scale down to fit quadrant IV
    else: y = .5 * a(j)      # step is 0, ergo function a
    return y + .5           # scale down and lift to quad II
def rampU(x, a, b):      # Ramp Up
    # two functions, a,b, combined. steps = 2
    step, j = remap(2, x)  # step is either 0 or 1
    if step:                # step is 1, ergo function b
        y = .5 * b(j)       # scale down and lift to quad I
        return y + .5
    else: return .5 * a(j)  # step is 0, ergo function a
                            # scale down to fit quadrant III
def sin_halfF(x):
    y = twofer(x, curveF, curveV)
    return y
def sin_halfH(x):
    return twofer(x, curveH, curveB)
def sin_whole(x):
    return rampD(x, sin_halfF, sin_halfH)

def repetitions(x, numSteps, function):
    step, j = remap(numSteps, x)    # repeat combo numSteps number of times
    # print(numSteps, step, j)
    y = function(j)                 # call function
    return y

def repetitions2(x, numSteps, function):
    step, j = remap(numSteps, x)    # repeat combo numSteps number of times
    height = step * (1/numSteps)
    y = function(j) + height                # call function
    return y




def twofer(x, a, b):
    # two functions, a,b, combined. steps = 2
    step, j = remap(2, x)      # step is either 0 or 1
    if step: y = b(j)     # step is 1, ergo function b
    else: y = a(j)        # step is 0, ergo function a
    return y

def doubleU(x, function):
    # a) function reduced to quad III, then (b) repeated in quad I
    step, j = remap(2, x)    # step is either 0 or 1
    y = .5 * function(j)      # compute y; scale to half height
    if step:             # step is 1, ergo function (b)
        return y + .5    # lift to quad I
    else: return y       # step is 0, ergo function a in quad III

def upper(x):
    return rampU(x,curveB, curveF )

def square_wave(x):
    # two functions, a,b, combined. steps = 2
    step, j = tremap(2, x)      # step is either 0 or 1
    if step: y = 1.0    # step is 1, ergo y is high (1.0)
    else: y = 0         # step is 0, ergo y is low (0)
    return y            # could be reduced to just "return step"

def do_this(x, function, numSteps, style):
    step, j = tremap(numSteps, x)  # repeat function, numSteps number of times
    if (style == "H") or (style == "B"): j = 1 - j  # H or B
    y = function(j)  # F
    if (style == "V") or (style == "B"): y = 1 - y  # V or B
    return y

def sequence(x, step):
    y = funlist[step](x)
    return y

def sin_slice_f(x):        # first quarter of sin curve: 0-90 degrees
    a = (x * PI / 2);
    y = math.sin(a)
    return y

def sin_slice_v(x):        # first quarter of sin curve: 0-90 degrees; mirrored "V"
    a = (x * PI / 2);
    y = 1 - math.sin(a)
    return y

def sin_slice_h(x):        # first quarter of sin curve: 0-90 degrees
    x = 1 - x
    a = (x * PI / 2);
    y = math.sin(a)
    return y

def sin_slice_b(x):        # first quarter of sin curve: 0-90 degrees
    x = 1 - x
    a = (x * PI / 2);
    y = 1 - math.sin(a)
    return y

def line_f(x):
    return x

def line_v(x):
    return 1 - x

funlist = [sin_slice_f, sin_slice_h, sin_slice_v, sin_slice_b, sin_slice_f,
           square_wave,square_wave, sin_slice_f, sin_slice_v,
           sin_slice_v, sin_slice_h, line_f, line_v,
           square_wave, square_wave, square_wave, square_wave]


"""

to rotate normalized point around center of screen:
move to origin: -(.5,.5)
rotate:  (x,y) -> (y, -x)
move back:  +(.5,5,)

clockwise rotation:
90 deg.: (y, -x)
270 deg: (-y, x)
 
"""

