### OSKAR preamble

import bpy
import bmesh
import inspect
import sys
import math
from mathutils import Vector, Euler, Color
import time

osk_slider_names = []

osk_on_slider_update = None

def osk_slider_update(self, context):
    osk_on_slider_update()

class OskSliders(object):
    def new(self, name, **kwargs):
        osk_slider_names.append(name)
        setattr(bpy.types.Scene, name, bpy.props.FloatProperty(update=osk_slider_update, **kwargs))
    
    def __getattr__(self, name):
        return getattr(bpy.context.scene, name)

class OskarSlidersPanel(bpy.types.Panel):
    bl_label = "Sliders"
    bl_idname = "OBJECT_PT_OSKAR"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'OSKAR'

    def draw(self, context):
        layout = self.layout
        for name in osk_slider_names:
            layout.prop(context.scene, name)

bpy.utils.register_class(OskarSlidersPanel)

Sliders = OskSliders()

osk_default_material = (0.5, 0, 1)

class DynamicVar:
    def __init__(self, default):
        self.stack = [default]
    
    @property
    def value(self):
        return self.stack[-1]

    def bind(self, value):
        self.stack.append(value)
    
    def unbind(self):
        if len(self.stack) > 1:
            self.stack.pop()
        else:
            raise RuntimeError("Cannot unbind default value")

    def __enter__(self):
        return self.value

    def __exit__(self, exc_type, exc_value, tb):
        self.unbind()

    def __call__(self, value):
        self.bind(value)
        return self

__time__ = DynamicVar(0)
__material__ = DynamicVar(osk_default_material)
__visible__ = DynamicVar(True)

def sin(x:float) -> float:
    """
    Calculate the sine of an angle given in degrees.
    """
    return math.sin(math.radians(x))

def cos(x:float) -> float:
    """
    Calculate the cosine of an angle given in degrees.
    """
    return math.cos(math.radians(x))

def look_at(camera:tuple[float,float,float], target:tuple[float,float,float]) -> tuple[float,float,float]:
    """
    Calculate the Euler angles for a camera to look at a target point.
    """
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

def osk_points_to_curve(points, spline_type="NURBS", smoothness=2, resolution=64, name="Curve", closed=False, data=None):
    if data is None:
        data = bpy.data.curves.new("Line", 'CURVE')
        spline = data.splines.new(spline_type)
    else:
        spline = data.splines[0]
    if spline.point_count_u < len(points):
        spline.points.add(len(points) - spline.point_count_u)
    for i in range(len(points)):
        spline.points[i].co = Vector((*points[i], 1))
    spline.use_endpoint_u = True
    spline.use_cyclic_u = closed
    spline.order_u = smoothness
    spline.resolution_u = resolution
    return data

class Ribbon(Node):
    """
    Ribbon primitive
    """
    def __init__(self, points=[], cross_section=[], start=0, stop=1, smoothness=2, bevel_resolution=16, spline_resolution=64, twist_mode='TANGENT', twist_smooth=0.0):
        values = (points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution, twist_mode, twist_smooth)
        super().__init__(values)
    
    def mount(self, root):
        points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution, twist_mode, twist_smooth = self.values
        material = __material__.value
        visible = __visible__.value
        line_data = osk_points_to_curve(points, "POLY", smoothness, spline_resolution)
        self.ref = bpy.data.objects.new("Line", line_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)

        cross_section_data = osk_points_to_curve(cross_section, "NURBS", smoothness, spline_resolution, closed=True)
        cross_section_object = bpy.data.objects.new("CrossSection", cross_section_data)
        cross_section_object.hide_render = True
        cross_section_object.hide_viewport = True
        bpy.context.collection.objects.link(cross_section_object)

        line_data.bevel_mode = 'OBJECT'
        line_data.dimensions = '3D'
        line_data.twist_mode = twist_mode
        line_data.twist_smooth = twist_smooth
        line_data.use_fill_caps = True
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_object = cross_section_object
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop

        osk_set_visible(self.ref, visible)
        self.ref.data.materials.append(osk_make_material(material))

    def update(self, old_values):
        points, cross_section, start, stop, smoothness, bevel_resolution, spline_resolution, twist_mode, twist_smooth = self.values
        material = __material__.value
        visible = __visible__.value
        old_points, old_cross_section, old_start, old_stop, old_smoothness, old_bevel_resolution, old_spline_resolution, old_twist_mode, old_twist_smooth = old_values

        if points != old_points:
            osk_points_to_curve(points, "POLY", smoothness, spline_resolution, data=self.ref.data)
        
        if cross_section != old_cross_section:
            osk_points_to_curve(cross_section, "NURBS", smoothness, spline_resolution, closed=True, data=self.ref.data.bevel_object.data)

        self.ref.data.bevel_resolution = bevel_resolution
        self.ref.data.bevel_factor_start = start
        self.ref.data.bevel_factor_end = stop

        if material is not None:
            h, s, v = material
            color = Color()
            color.hsv = (h, s, v)
            self.ref.material_slots[self.ref.active_material_index].material.node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (color.r, color.g, color.b, 1)
        osk_set_visible(self.ref, visible)

class Line(Node):
    """
    Line primitive
    """
    def __init__(self, points=[], thickness=0.05, start=0, stop=1, smoothness=2, bevel_resolution=16, spline_resolution=64):
        values = (points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution)
        super().__init__(values)
    
    def mount(self, root):
        points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        line_data = bpy.data.curves.new("Line", 'CURVE')
        self.ref = bpy.data.objects.new("Line", line_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
        osk_set_visible(self.ref, True)

        line_data.bevel_mode = 'ROUND'
        line_data.dimensions = '3D'
        line_data.use_fill_caps = True
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_depth = thickness
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop

        spline = line_data.splines.new('NURBS')
        spline.points.add(len(points) - len(spline.points))
        for i in range(len(spline.points)):
            spline.points[i].co = Vector((*points[i], 1))
        spline.use_endpoint_u = True
        spline.order_u = smoothness
        spline.resolution_u = spline_resolution
    
    def update(self, _old_values):
        points, thickness, start, stop, smoothness, bevel_resolution, spline_resolution = self.values
        line_data = self.ref.data
        osk_set_visible(self.ref, True) # not clear why we have to do this
        line_data.bevel_resolution = bevel_resolution
        line_data.bevel_depth = thickness
        line_data.bevel_factor_start = start
        line_data.bevel_factor_end = stop
        spline = line_data.splines[0]
        for i in range(len(spline.points)):
            spline.points[i].co = Vector((*points[i], 1))
        spline.order_u = smoothness
        spline.resolution_u = spline_resolution

class GeometricPrimitive(Node):
    def __init__(self, type):
        self.type = type
        material = __material__.value
        visible = __visible__.value
        super().__init__((material, visible))
    
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
    """
    Cube primitive
    """
    def __init__(self):
        super().__init__("Cube")

class Square(GeometricPrimitive):
    """
    Square primitive
    """
    def __init__(self):
        super().__init__("Plane")

class Cylinder(GeometricPrimitive):
    """
    Cylinder primitive
    """
    def __init__(self):
        super().__init__("Cylinder")

class Sphere(GeometricPrimitive):
    """
    Sphere primitive
    """
    def __init__(self):
        super().__init__("Sphere")

def disc(radius_outer=1, radius_inner=0, angle_start=0, angle_end=360, resolution=32) -> list[tuple[float, float, float]]:
    """
    Generate a list of points representing a disc in 2D space
    """
    points = []
    angle_diff = angle_end - angle_start
    step = angle_diff / resolution
    if radius_inner == 0:
        points.append((0, 0, 0))
    for i in range(resolution+1):
        x = cos(angle_start + i * step) * radius_outer
        y = sin(angle_start + i * step) * radius_outer
        points.append((x, y, 0))
    if radius_inner != 0:
        for i in reversed(range(resolution+1)):
            x = cos(angle_start + i * step) * radius_inner
            y = sin(angle_start + i * step) * radius_inner
            points.append((x, y, 0))
    return points

class Polygon(Node):
    """
    Polygon primitive
    """
    def __init__(self, points:list[tuple[float, float, float]]):
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
    """
    Prism primitive
    """
    def __init__(self, points:list[tuple[float, float, float]], depth=1):
        values = (points, depth)
        super().__init__(values)
    
    def mount(self, root):
        mesh = bpy.data.meshes.new(name="Prism")
        self.ref = bpy.data.objects.new("Prism", mesh)
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
    """
    Camera primitive

    TODO document the default orientation of camera
    """
    def __init__(self, type='PERSP', size=None):
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
    """
    Light primitive
    """
    def __init__(self, type='POINT', energy=1000):
        material = __material__.value
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
    def __init__(self, function, *args):
        pt = __time__.value
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

class Text(Node):
    """
    Text primitive
    """
    def __init__(self, body:str, font=None, extrude=0, offset=0, align_x='LEFT', align_y='TOP_BASELINE', bevel_depth=0):
        super().__init__((body, font, extrude, offset, align_x, align_y, bevel_depth))
    
    def mount(self, root):
        text_data = bpy.data.curves.new(type="FONT", name="Text")
        self.ref = bpy.data.objects.new("Text", text_data)
        self.ref.parent = root
        bpy.context.collection.objects.link(self.ref)
        self.update(self.values)
    
    def update(self, values):
        (body, font, extrude, offset, align_x, align_y, bevel_depth) = self.values
        self.ref.data.body = body
        self.ref.data.extrude = extrude
        self.ref.data.offset = offset
        self.ref.data.align_x = align_x
        self.ref.data.align_y = align_y
        self.ref.data.bevel_depth = bevel_depth
        if font is not None:
            font_data = bpy.data.fonts.load(font)
            self.ref.data.font = font_data
        else:
            self.ref.data.font = bpy.data.fonts['Bfont Regular']

osk_primitives = set()

def osk_is_primitive(func):
    return func.__name__ in osk_primitives

def primitive(func):
    """
    A decorator to mark a function as an Oskar primitive.
    """
    osk_primitives.add(func.__name__)
    return func

def osk_ensure_evaluated(val):
    if callable(val):
        return val()
    else:
        return val

def osk_reconcile(old, new):
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
            osk_reconcile(old.children[i], new.children[i])
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
        osk_reconcile(self.current, node)
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
    
    default_material = osk_make_material(osk_default_material)
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
    osk_initialize_scene()

    vscene = VirtualScene(picture())
    osk_enable_camera_view()

    def frame_change(scene):
        t = (scene.frame_current % scene.frame_end) / scene.frame_end
        with __time__(t):
            vscene.update(picture())

    bpy.app.handlers.frame_change_post.clear()    
    bpy.app.handlers.frame_change_post.append(frame_change)

    bpy.context.scene.frame_end = frames
    frame_change(bpy.context.scene)
    global osk_on_slider_update
    osk_on_slider_update = lambda: frame_change(bpy.context.scene)

### user code
