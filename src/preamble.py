### OSKAR preamble

import bpy
import bmesh
import inspect
import sys
import math
from mathutils import Vector, Euler, Color
import time

def sin(x):
    return math.sin(math.radians(x))

def cos(x):
    return math.cos(math.radians(x))

def look_at(camera, target):
    camera_location = Vector(camera)
    target_location = Vector(target)
    
    direction = target_location - camera_location
    direction.normalize()
    
    up = Vector((0, 1, 0))
    if abs(direction.dot(up)) > 0.99:
        up = Vector((1, 0, 0))
    
    quat_rotation = direction.to_track_quat('-Z', 'Y')
    euler_angles = quat_rotation.to_euler()

    return (math.degrees(euler_angles.x), math.degrees(euler_angles.y), math.degrees(euler_angles.z))

def osk_radians(xyz):
    return Euler((math.radians(xyz[0]), math.radians(xyz[1]), math.radians(xyz[2])))

def osk_set_visible(obj, state):
    obj.hide_set(not state)
    obj.hide_render = not state

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
    __slots__ = "ref", "values", "children", "parent"
    def __init__(self, values=None):
        self.ref = None
        self.values = values
        self.children = []
        self.parent = None 

    def mount(self, root):
        # call in subclasses after subclass logic
        for child in self.children:
            child.mount(self.ref)
    
    def update(self, _):
        pass

    def unmount(self):
        for child in self.children:
            child.unmount()
        bpy.data.objects.remove(self.ref)
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        return child
    
def osk_razor_thin(vec):
    x, y, z = vec
    return abs(x) < sys.float_info.epsilon or abs(y) < sys.float_info.epsilon or abs(z) < sys.float_info.epsilon

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
        self.name = name
        values = (t, r, s)
        super().__init__(values)
    
    def mount(self, root):
        _t, _r, _s = self.values
        self.ref = bpy.data.objects.new(self.name, None)
        self.ref.parent = root
        self.update(self.values)
        bpy.context.collection.objects.link(self.ref)
        super().mount(root)
    
    def update(self, _values):
        t, r, s = self.values
        self.ref.location = Vector(t)
        self.ref.rotation_euler = osk_radians(r)
        self.ref.scale = Vector(s)

def points_to_curve(points, spline_type="NURBS", smoothness=2, resolution=64, name="Curve", closed=False, data=None):
    if data is None:
        data = bpy.data.curves.new("Line", 'CURVE')
        spline = data.splines.new(spline_type)
    else:
        spline = data.splines[0]
    spline.use_endpoint_u = True
    spline.use_cyclic_u = closed
    spline.order_u = smoothness
    spline.resolution_u = resolution
    if spline.point_count_u < len(points):
        spline.points.add(len(points) - spline.point_count_u)
    for i in range(len(points)):
        spline.points[i].co = Vector((*points[i], 1))
    return data

class Ribbon(Node):
    def __init__(self, _pt, _context, points=[], cross_section=[], start=0, stop=1, smoothness=2, bevel_resolution=16, spline_resolution=64):
        values = (points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution)
        super().__init__(values)
    
    def mount(self, root):
        points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        line_data = points_to_curve(points, "POLY", smoothness, spline_resolution)
        self.ref = bpy.data.objects.new("Line", line_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)

        cross_section_data = points_to_curve(cross_section, "NURBS", smoothness, spline_resolution, closed=True)
        cross_section_object = bpy.data.objects.new("CrossSection", cross_section_data)
        cross_section_object.hide_render = True
        cross_section_object.hide_viewport = True
        bpy.context.collection.objects.link(cross_section_object)

        line_data.bevel_mode = 'OBJECT'
        line_data.dimensions = '3D'
        line_data.use_fill_caps = True
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_object = cross_section_object
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop

    def update(self, old_values):
        points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        old_points, old_cross_section, old_start, old_stop, old_smoothness, old_bevel_resolution, old_spline_resolution = old_values

        if points != old_points:
            points_to_curve(points, "POLY", smoothness, spline_resolution, data=self.ref.data)
        
        if cross_section != old_cross_section:
            points_to_curve(cross_section, "NURBS", smoothness, spline_resolution, closed=True, data=self.ref.data.bevel_object.data)

        self.ref.data.bevel_resolution = bevel_resolution
        self.ref.data.bevel_factor_start = start
        self.ref.data.bevel_factor_end = stop

class Line(Node):
    def __init__(self, _pt, _context, points=[], thickness=0.05, start=0, stop=1, smoothness=2, bevel_resolution=16, spline_resolution=64):
        values = (points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution)
        super().__init__(values)
    
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
    
    def update(self, _old_values):
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
    def __init__(self, type, context):
        self.type = type
        super().__init__(context)
    
    def mount(self, root):
        geo_data = bpy.data.meshes[self.type]
        self.ref = bpy.data.objects.new(self.type, geo_data)
        bpy.context.collection.objects.link(self.ref)
        self.ref.parent = root
        material, visible = self.values
        osk_set_visible(self.ref, visible)
        if material is not None:
            self.ref.material_slots[self.ref.active_material_index].link = 'OBJECT'
            self.ref.material_slots[self.ref.active_material_index].material = osk_make_material(material)
    
    def update(self, _old_values):
        material, visible = self.values
        if material is not None:
            h, s, v = material
            color = Color()
            color.hsv = (h, s, v)
            self.ref.material_slots[self.ref.active_material_index].material.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (color.r, color.g, color.b, 1)
        osk_set_visible(self.ref, visible)

class Cube(GeometricPrimitive):
    def __init__(self, _pt, context):
        super().__init__("Cube", context)

class Square(GeometricPrimitive):
    def __init__(self, _pt, context):
        super().__init__("Plane", context)

class Cylinder(GeometricPrimitive):
    def __init__(self, _pt, context):
        super().__init__("Cylinder", context)

class Sphere(GeometricPrimitive):
    def __init__(self, _pt, context):
        super().__init__("Sphere", context)

def disc(radius=1, angle_start=0, angle_end=360, radius_inner=0, resolution=32):
    points = []
    angle_diff = angle_end - angle_start
    step = angle_diff / resolution
    if radius_inner == 0:
        points.append((0, 0, 0))
    for i in range(resolution+1):
        x = cos(angle_start + i * step) * radius
        y = sin(angle_start + i * step) * radius
        points.append((x, y, 0))
    if radius_inner != 0:
        for i in reversed(range(resolution+1)):
            x = cos(angle_start + i * step) * radius_inner
            y = sin(angle_start + i * step) * radius_inner
            points.append((x, y, 0))
    return points

class Polygon(Node):
    def __init__(self, _pt, _context, points):
        super().__init__(points)
    
    def mount(self, root):
        mesh = bpy.data.meshes.new(name="Polygon")
        self.ref = bpy.data.objects.new("Polygon", mesh)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
        self.update()

    def update(self, _old_values=None):
        bm = bmesh.new()
        bm.faces.new([bm.verts.new(pt) for pt in self.values])
        bm.to_mesh(self.ref.data)
        bm.free()

class Prism(Node):
    def __init__(self, _pt, _context, points, depth=1):
        values = (points, depth)
        super().__init__(values)
    
    def mount(self, root):
        mesh = bpy.data.meshes.new(name="Polygon")
        self.ref = bpy.data.objects.new("Polygon", mesh)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
        self.update()

    def update(self, _old_values=None):
        points, depth = self.values
        bm = bmesh.new()
        base_points =[bm.verts.new(pt) for pt in points]
        v10 = base_points[1].co - base_points[0].co
        v20 = base_points[2].co - base_points[0].co
        normal = v10.cross(v20)
        normal.normalize()
        extruded_points = [bm.verts.new(p.co + normal * depth) for p in base_points]
        bm.faces.new(base_points)
        bm.faces.new(extruded_points)
        length = len(extruded_points)
        for i in range(0, length):
            a = base_points[(i+0)%length]
            b = base_points[(i+1)%length]
            c = extruded_points[(i+1)%length]
            d = extruded_points[(i+0)%length]
            bm.faces.new([a, b, c, d])

        bm.to_mesh(self.ref.data)
        bm.free()


class Camera(Node):
    def __init__(self, _pt, _context, type='PERSP', size=None):
        self.type = type
        super().__init__(size)

    def mount(self, root):
        camera_data = bpy.data.cameras.new("Camera")
        self.ref = bpy.data.objects.new("Camera", camera_data)
        self.ref.parent = root
        camera_data.type = self.type
        bpy.context.scene.camera = self.ref
        bpy.context.collection.objects.link(self.ref)
        self.update(None)
    
    def update(self, _old_values):
        size = self.values
        if size is not None:
            if self.type == 'PERSP':
                self.ref.data.lens = size
            elif self.type == 'ORTHO':
                self.ref.data.ortho_scale = size


class Light(Node):
    def __init__(self, _pt, context, type='POINT', energy=1000):
        material, visible = context
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

    def update(self, _old_values):
        material, energy = self.values
        h, s, v = material
        color = Color()
        color.hsv = (h, s, v)
        self.ref.data.color = color
        self.ref.data.energy = energy

class Primitive(Node):
    __slots__ = "function"
    def __init__(self, function, pt, context, *args):
        self.function = function
        super().__init__((pt, args))
    
    def update(self, _values):
        root = self.ref.parent
        self.unmount()
        self.mount(root)
    
    def mount(self, root):
        pt, args = self.values
        self.ref = self.function(pt, *args)
        self.ref.parent = root

osk_primitives = set()

def osk_is_primitive(func):
    return func.__name__ in osk_primitives

def primitive(func):
    osk_primitives.add(func.__name__)
    return func

def reconcile(old, new):
    if type(old) != type(new):
        root = old.parent.ref if old.parent is not None else None
        old.unmount()
        new.mount(root)
    else:
        new.ref = old.ref
        if not old.values == new.values:
            new.update(old.values)
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
    # (material, visible)
    root_context = (None, True)
    osk_initialize_scene()

    vscene = VirtualScene(picture(0, root_context))
    osk_enable_camera_view()

    def frame_change(scene):
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        vscene.update(picture(t, root_context))

    bpy.app.handlers.frame_change_post.clear()    
    bpy.app.handlers.frame_change_post.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)

### user code
