### OSKAR preamble

import bpy
import math
from mathutils import Vector, Euler, Color
import time

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def osk_radians(xyz):
    return Euler((math.radians(xyz[0]), math.radians(xyz[1]), math.radians(xyz[2])))

def osk_make_material(data):
    h, s, v = data
    color = Color()
    color.hsv = (h, s, v)
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new(type='ShaderNodeOutputMaterial')
    shader = nodes.new(type='ShaderNodeBsdfDiffuse')
    nodes["Diffuse BSDF"].inputs[0].default_value = (color.r, color.g, color.b, 1)
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
        for child in self.children:
            child.unmount()
        bpy.data.objects.remove(self.ref)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        return child
    
    def update(self, _):
        pass

class Transform(Node):
    def __init__(self, name="Transform", translate=[], rotate=[], scale=[]):
        t = Vector()
        r = Vector()
        s = Vector((1,1,1))
        for v in translate:
            t += Vector(v)
        for v in rotate:
            r += Vector(v)
        for v in scale:
            s *= Vector(v)
        values = (name, t, r, s)
        super().__init__(values)
    
    def mount(self, root):
        name, _t, _r, _s = self.values
        self.ref = bpy.data.objects.new(name, None)
        self.ref.parent = root
        self.update(self.values)
        bpy.context.collection.objects.link(self.ref)
        super().mount(root)
    
    def update(self, values):
        _name, t, r, s = values
        self.ref.location = Vector(t)
        self.ref.rotation_euler = osk_radians(r)
        self.ref.scale = Vector(s)

# class Ribbon(Node):
#     def __init__(self, points):
#         super().__init__(points)

#     def update(self, values):
#         t, r, s = values
#         self.ref.location = Vector(t)
#         self.ref.rotation_euler = osk_radians(r)
#         self.ref.scale = Vector(s)

#     def mount(self, root):
#         curve_data = bpy.data.curves.new("Ribbon", 'CURVE')
#         self.ref = bpy.data.objects.new("Ribbon", curve_data)
#         self.ref.parent = root
#         bpy.context.collection.objects.link(self.ref)

class Line(Node):
    def __init__(self, _pt, _material, points=[], thickness=0.05, start=0, stop=1, smoothness=2, bevel_resolution=16, spline_resolution=64):
        values = (points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution)
        super().__init__(_pt, _material, values)
    
    def mount(self, root):
        points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        line_data = bpy.data.curves.new("Line", 'CURVE')
        self.ref = bpy.data.objects.new("Line", line_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)

        line_data.bevel_mode = 'ROUND'
        line_data.dimensions = '3D'
        line_data.use_fill_caps = True
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_depth = thickness
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop

        spline = line_data.splines.new('NURBS')
        spline.use_endpoint_u = True
        spline.order_u = smoothness
        spline.resolution_u = spline_resolution
        spline.points.add(len(points))
        for i in range(len(points)):
            spline.points[i].co = Vector((*points[i], 1))
    
    def update(self, _values):
        points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        line_data = self.ref.data
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_depth = thickness
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop
        spline = line_data.splines[0]
        spline.order_u = smoothness
        spline.resolution_u = spline_resolution
        for i in range(len(points)):
            spline.points[i].co = Vector((*points[i], 1))

class GeometricPrimitive(Node):
    def __init__(self, type, material):
        self.type = type
        super().__init__(material)
    
    def mount(self, root):
        geo_data = bpy.data.meshes[self.type]
        self.ref = bpy.data.objects.new(self.type, geo_data)
        bpy.context.collection.objects.link(self.ref)
        self.ref.parent = root
        if self.values is not None:
            self.ref.material_slots[self.ref.active_material_index].link = 'OBJECT'
            self.ref.material_slots[self.ref.active_material_index].material = osk_make_material(self.values)
    
    def update(self, values):
        h, s, v = self.values
        color = Color()
        color.hsv = (h, s, v)
        self.ref.material_slots[self.ref.active_material_index].material.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (color.r, color.g, color.b, 1)

class Cube(GeometricPrimitive):
    def __init__(self, _pt, material):
        super().__init__("Cube", material)

class Square(GeometricPrimitive):
    def __init__(self, _pt, material):
        super().__init__("Plane", material)

class Cylinder(GeometricPrimitive):
    def __init__(self, _pt, material):
        super().__init__("Cylinder", material)

class Sphere(GeometricPrimitive):
    def __init__(self, _pt, material):
        super().__init__("Sphere", material)

class Camera(Node):
    def __init__(self, _pt, _material):
        super().__init__()

    def mount(self, root):
        camera_data = bpy.data.cameras.new("Camera")
        self.ref = bpy.data.objects.new("Camera", camera_data)
        self.ref.parent = root
        bpy.context.scene.camera = self.ref
        bpy.context.collection.objects.link(self.ref)

class Light(Node):
    def __init__(self, _pt, material, type='POINT', energy=1000):
        self.type = type
        values = (material, energy)
        super().__init__(values)
    
    def mount(self, root):
        material, energy = self.values
        light_data = bpy.data.lights.new("Light", type=self.type)
        light_data.energy = energy
        h, s, v = material
        color = Color()
        color.hsv = (h, s, v)
        light_data.color = color
        self.ref = bpy.data.objects.new("Light", light_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)

    def update(self, values):
        material, energy = self.values
        h, s, v = material
        color = Color()
        color.hsv = (h, s, v)
        self.ref.data.color = color
        self.ref.data.energy = energy

# class Primitive(Node):
#     __slots__ = "function"
#     def __init__(self, function, args=()):
#         self.function = function
#         super().__init__(args)
    
#     def update(self, _):
#         root = self.ref.parent
#         self.unmount(root)
#         self.mount(root)
    
#     def mount(self, root):
#         self.ref = self.function(*self.values)
#         self.ref.parent = root
#         super().mount(root)
    
#     def unmount(self, root):
#         super().unmount(root)
#         bpy.data.objects.remove(self.ref)

def reconcile(old, new):
    if type(old) != type(new):
        root = old.parent.ref if old.parent is not None else None
        old.unmount()
        new.mount(root)
    else:
        new.ref = old.ref
        if not old.values == new.values:
            new.update(new.values)
        old_children = len(old.children)
        new_children = len(new.children)
        shortest_children = min(old_children, new_children)
        for i in range(0, shortest_children):
            reconcile(old.children[i], new.children[i])
        if old_children > new_children:
            for i in range(shortest_children, old_children):
                old.children[i].unmount()
        else:
            for i in range(shortest_children, new_children):
                new.children[i].mount(new.ref)

class VirtualScene:
    __slots__ = "current"
    def __init__(self, node):
        self.current = node
        node.mount(None)
    
    def update(self, node):
        reconcile(self.current, node)
        self.current = node

def osk_initialize_material(object, material):
    object.data.materials.append(material)
    object.material_slots[object.active_material_index].link = 'OBJECT'


def osk_initialize_scene():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)
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
    
    default_material = osk_make_material((0.5, 1, 1))
    osk_initialize_material(bpy.data.objects['Cube'], default_material)
    osk_initialize_material(bpy.data.objects['Plane'], default_material)
    osk_initialize_material(bpy.data.objects['Cylinder'], default_material)
    osk_initialize_material(bpy.data.objects['Sphere'], default_material)

# https://blender.stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
def osk_enable_camera_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'CAMERA'
            break

def osk_film(picture, frames):
    osk_initialize_scene()

    vscene = VirtualScene(picture(0))
    osk_enable_camera_view()

    def frame_change(scene):
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        vscene.update(picture(t))

    bpy.app.handlers.frame_change_post.clear()    
    bpy.app.handlers.frame_change_post.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)

### user code
