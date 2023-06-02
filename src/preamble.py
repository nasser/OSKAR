### OSKAR preamble

import bpy
import math
from mathutils import Vector, Euler
import time

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def osk_radians(x, y, z):
    return Euler((math.radians(x), math.radians(y), math.radians(z)))

def osk_translate(obj, x, y, z):
    obj.location += Vector((x, y, z))

def osk_rotate(obj, x, y, z):
    obj.rotation_euler.rotate(osk_radians(x, y, z))

def osk_scale(obj, x, y, z):
    obj.scale *= Vector((x, y, z))

def osk_clean_scene():
    for obj in bpy.context.collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

## TODO keep primitives in their own collection
_cube = None
_square = None
_cylinder = None
_sphere = None

def osk_start_frame():
    global _cube
    global _square
    global _cylinder
    global _sphere
    _cube = None
    _square = None
    _cylinder = None
    _sphere = None
    osk_clean_scene()

def Cube(root=None, _pt=0):
    global _cube
    if _cube is None:
        bpy.ops.mesh.primitive_cube_add()
        _cube = bpy.context.object
        _cube.hide_viewport = True
    copy = _cube.copy()
    copy.hide_viewport = False
    copy.parent = root
    bpy.context.collection.objects.link(copy)
    return copy

def Square(root=None, _pt=0):
    global _square
    if _square is None:
        bpy.ops.mesh.primitive_plane_add()
        _square = bpy.context.object
        _square.hide_viewport = True
    copy = _square.copy()
    copy.hide_viewport = False
    copy.parent = root
    bpy.context.collection.objects.link(copy)
    return copy

def Cylinder(root=None, _pt=0):
    global _cylinder
    if _cylinder is None:
        bpy.ops.mesh.primitive_cylinder_add()
        _cylinder = bpy.context.object
        _cylinder.hide_viewport = True
    copy = _cylinder.copy()
    copy.hide_viewport = False
    copy.parent = root
    bpy.context.collection.objects.link(copy)
    return copy

def Sphere(root=None, _pt=0):
    global _sphere
    if _sphere is None:
        bpy.ops.mesh.primitive_uv_sphere_add()
        _sphere = bpy.context.object
        _sphere.hide_viewport = True
    copy = _sphere.copy()
    copy.hide_viewport = False
    copy.parent = root
    bpy.context.collection.objects.link(copy)
    return copy

def Camera(root=None, _pt=0):
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    camera.parent = root
    bpy.context.collection.objects.link(camera)
    return camera

def Light(root=None, pt=0, type='POINT'):
    light_data = bpy.data.lights.new(name="Light", type=type)
    light = bpy.data.objects.new("Light", light_data)
    light.parent = root
    bpy.context.collection.objects.link(light)
    return light

def Empty(root=None, _pt=0):
    o = bpy.data.objects.new( "empty", None )
    o.parent = root
    bpy.context.collection.objects.link(o)
    return o

def osk_film(picture, frames):
    def frame_change(scene):
        osk_start_frame()
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        picture(None, t)
        bpy.ops.object.select_all(action='DESELECT')

    bpy.app.handlers.frame_change_pre.clear()    
    bpy.app.handlers.frame_change_pre.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)

### user code
