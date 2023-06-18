### OSKAR preamble

import bpy
import math
from mathutils import Vector, Euler
import time

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def osk_radians(xyz):
    return Euler((math.radians(xyz[0]), math.radians(xyz[1]), math.radians(xyz[2])))

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

class Node:
    def __init__(self, values=None):
        self.ref = None
        self.values = values
        self.children = []
        self.parent = None 

    def mount(self, root):
        # call in subclasses after subclass logic
        for child in self.children:
            child.mount(self.ref)
    
    def unmount(self):
        # call in subclasses before subclass logic
        for child in self.children:
            child.unmount()
        bpy.data.objects.remove(self.ref)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        return child
    
    def update(self):
        pass

class Transform(Node):
    def __init__(self, translate=[], rotate=[], scale=[]):
        t = Vector()
        r = Vector()
        s = Vector((1,1,1))
        for v in translate:
            t += Vector(v)
        for v in rotate:
            r += Vector(v)
        for v in scale:
            s *= Vector(v)
        values = (t, r, s)
        super().__init__(values)
    
    def mount(self, root):
        self.ref = bpy.data.objects.new("Empty", None )
        self.ref.parent = root
        self.update(self.values)
        bpy.context.collection.objects.link(self.ref)
        super().mount(root)
    
    def update(self, values):
        t, r, s = values
        self.ref.location = Vector(t)
        self.ref.rotation_euler = osk_radians(r)
        self.ref.scale = Vector(s)

class Cube(Node):
    def mount(self, root):
        cube_data = bpy.data.meshes["Cube"]
        self.ref = bpy.data.objects.new("Cube", cube_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Square(Node):
    def mount(self, root):
        plane_data = bpy.data.meshes["Plane"]
        self.ref = bpy.data.objects.new("Square", plane_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Cylinder(Node):
    def mount(self, root):
        plane_data = bpy.data.meshes["Cylinder"]
        self.ref = bpy.data.objects.new("Square", plane_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Sphere(Node):
    def mount(self, root):
        plane_data = bpy.data.meshes["Sphere"]
        self.ref = bpy.data.objects.new("Square", plane_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Camera(Node):
    def mount(self, root):
        camera_data = bpy.data.cameras.new("Camera")
        self.ref = bpy.data.objects.new("Camera", camera_data)
        self.ref.parent = root
        bpy.context.scene.camera = self.ref
        bpy.context.collection.objects.link(self.ref)

class Light(Node):
    def __init__(self, type='POINT', energy=1000):
        values = (type, energy)
        super().__init__(values)
    
    def mount(self, root):
        type, energy = self.values
        light_data = bpy.data.lights.new("Light", type=type)
        light_data.energy = energy
        self.ref = bpy.data.objects.new("Light", light_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)

class Primitive(Node):
    __slots__ = "function"
    def __init__(self, function, args=()):
        self.function = function
        super().__init__(args)
    
    def update(self, _):
        root = self.ref.parent
        self.unmount(root)
        self.mount(root)
    
    def mount(self, root):
        self.ref = self.function(*self.values)
        self.ref.parent = root
        super().mount(root)
    
    def unmount(self, root):
        super().unmount(root)
        bpy.data.objects.remove(self.ref)

def reconcile(old, new):
    if type(old) != type(new):
        root = old.parent.ref if old.parent is not None else None
        old.unmount()
        new.mount(root)
    else:
        new.ref = old.ref
        if not old.values == new.values:
            new.update(new.values)
        shortest_children = min(len(old.children), len(new.children))
        for i in range(0, shortest_children):
            reconcile(old.children[i], new.children[i])
        if len(old.children) > len(new.children):
            for i in range(shortest_children, len(old.children)):
                old.children[i].unmount()
        else:
            for i in range(shortest_children, len(new.children)):
                new.children[i].mount(new.ref)

class VirtualScene:
    __slots__ = "current"
    def __init__(self, node):
        self.current = node
        node.mount(None)
    
    def update(self, node):
        reconcile(self.current, node)
        self.current = node

def osk_initialize_scene():
    for obj in bpy.context.collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.ops.mesh.primitive_cube_add()
    bpy.context.object.hide_render = True
    bpy.context.object.hide_viewport = True
    bpy.ops.mesh.primitive_plane_add()
    bpy.context.object.hide_render = True
    bpy.context.object.hide_viewport = True
    bpy.ops.mesh.primitive_cylinder_add()
    bpy.context.object.hide_render = True
    bpy.context.object.hide_viewport = True
    bpy.ops.mesh.primitive_uv_sphere_add()
    bpy.context.object.hide_render = True
    bpy.context.object.hide_viewport = True

def osk_film(picture, frames):
    osk_initialize_scene()

    vscene = VirtualScene(picture(0))

    def frame_change(scene):
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        vscene.update(picture(t))

    bpy.app.handlers.frame_change_post.clear()    
    bpy.app.handlers.frame_change_post.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)

### user code
