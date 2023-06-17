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
    def __init__(self):
        super().__init__(None)
    
    def mount(self, root):
        cube_data = bpy.data.meshes["Cube"]
        self.ref = bpy.data.objects.new("Cube", cube_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Square(Node):
    def __init__(self):
        super().__init__(None)
    
    def mount(self, root):
        plane_data = bpy.data.meshes["Plane"]
        self.ref = bpy.data.objects.new("Square", plane_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Cylinder(Node):
    def __init__(self):
        super().__init__(None)
    
    def mount(self, root):
        plane_data = bpy.data.meshes["Cylinder"]
        self.ref = bpy.data.objects.new("Square", plane_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
    
class Sphere(Node):
    def __init__(self):
        super().__init__(None)
    
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

class PatchReplaceNode:
    __slots__ = "old_node", "new_node"
    def __init__(self, old_node, new_node):
        self.old_node = old_node
        self.new_node = new_node

class PatchAddNode:
    __slots__ = "node", "parent"
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent

class PatchRemoveNode:
    __slots__ = "node"
    def __init__(self, node):
        self.node = node

class PatchUpdateValues:
    __slots__ = "node", "values"
    def __init__(self, node, values):
        self.node = node
        self.values = values

class PatchCopyRef:
    __slots__ = "from_node", "to_node"
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

def diff(a, b, patch=[]):
    if type(a) != type(b):
        patch.append(PatchReplaceNode(a, b))
    else:
        patch.append(PatchCopyRef(a, b))
        if not a.values == b.values:
            patch.append(PatchUpdateValues(a, b.values))
        shortest_children = min(len(a.children), len(b.children))
        for i in range(0, shortest_children):
            a_child = a.children[i]
            b_child = b.children[i]
            diff(a_child, b_child, patch)
        if len(a.children) > len(b.children):
            for i in range(shortest_children, len(a.children)):
                patch.append(PatchRemoveNode(a.children[i]))
        else:
            for i in range(shortest_children, len(b.children)):
                patch.append(PatchAddNode(b.children[i], a))
    return patch

def apply(patch):
    for op in patch:
        match op:
            case PatchReplaceNode():
                root = op.old_node.parent.ref if op.old_node.parent is not None else None
                op.old_node.unmount(root)
                op.old_node.mount(root)

            case PatchAddNode():
                op.node.mount(op.parent.ref)
                op.node.parent = op.parent

            case PatchRemoveNode():
                root = op.node.parent.ref if op.node.parent is not None else None
                op.node.unmount(root)

            case PatchUpdateValues():
                op.node.values = op.values
                op.node.update(op.values)
                
            case PatchCopyRef():
                op.to_node.ref = op.from_node.ref

class VirtualScene:
    __slots__ = "current"
    def __init__(self, node):
        self.current = node
        node.mount(None)
    
    def update(self, node):
        apply(diff(self.current, node))
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
