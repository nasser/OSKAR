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

def osk_material(r, g, b):
    data = (r, g, b)
    return data

def osk_make_material(data):
    r, g, b = data
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    shader = nodes.new(type='ShaderNodeBsdfDiffuse')
    nodes["Diffuse BSDF"].inputs[0].default_value = (r/255, g/255, b/255, 1)
    links.new(shader.outputs[0], output.inputs[0])
    return material

def osk_clean_scene():
    for obj in bpy.context.collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

def osk_start_frame():
    osk_clean_scene()


def Cube(root=None, _pt=0, material_data=None):
    # if _cube is None:
    #     bpy.ops.mesh.primitive_cube_add()
    #     # following line causes crash during render!
    #     #   Traceback (most recent call last):
    #     #   File "/Text", line 108, in9 frame_change
    #     #   File "/Text", line 138, in Scene
    #     #   File "/Text", line 54, in Cube
    #     #   AttributeError: 'Context' object has no attribute 'object'
    #     _cube = bpy.context.object
    #     _cube.hide_viewport = True

    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.object
    if material_data is not None:
        material = osk_make_material(material_data)
        cube.data.materials.append(material)
    cube.parent = root

def Square(root=None, _pt=0, material_data=None):
    bpy.ops.mesh.primitive_plane_add()
    square = bpy.context.object
    if material_data is not None:
        material = osk_make_material(material_data)
        square.data.materials.append(material)
    square.parent = root

def Cylinder(root=None, _pt=0, material_data=None):
    bpy.ops.mesh.primitive_cylinder_add()
    cylinder = bpy.context.object
    if material_data is not None:
        material = osk_make_material(material_data)
        cylinder.data.materials.append(material)
    cylinder.parent = root

def Sphere(root=None, _pt=0, material_data=None):
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    if material_data is not None:
        material = osk_make_material(material_data)
        sphere.data.materials.append(material)
    sphere.parent = root

def Camera(root=None, _pt=0, material_data=None):
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    camera.parent = root
    bpy.context.collection.objects.link(camera)
    return camera

def Light(root=None, pt=0, material_data=None, type='POINT', energy=1000):
    light_data = bpy.data.lights.new(name="Light", type=type)
    light_data.energy = energy
    if material_data is not None:
        light_data.color = material_data
    light = bpy.data.objects.new("Light", light_data)
    light.parent = root
    bpy.context.collection.objects.link(light)
    return light

def Empty(root=None, _pt=0, material=None):
    o = bpy.data.objects.new("Empty", None )
    o.parent = root
    bpy.context.collection.objects.link(o)
    return o

def osk_film(picture, frames):
    def frame_change(scene):
        osk_start_frame()
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        picture(None, t, None)
        bpy.ops.object.select_all(action='DESELECT')

    bpy.app.handlers.frame_change_pre.clear()    
    bpy.app.handlers.frame_change_pre.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)

### user code
