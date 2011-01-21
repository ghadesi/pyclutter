# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2011 Bastian Winkler <buz@netbuz.org>
#
# Clutter.py: Clutter overrides for introspection based bindings
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import sys
from ..overrides import override
from ..importer import modules
import keysyms

Clutter = modules['Clutter']._introspection_module

__all__ = ['keysyms']



def _to_color(anything):
    if isinstance(anything, Color):
        return anything
    elif isinstance(anything, (tuple, list)):
        return Color(*anything)
    elif isinstance(anything, str):
        return Color.from_string(anything)
    else:
        return None

def _to_actor_box(anything):
    if isinstance(anything, ActorBox):
        return anything
    elif isinstance(anything, (tuple, list)):
        return ActorBox(*anything)
    else:
        return None

def _to_geometry(anything):
    if isinstance(anything, Geometry):
        return anything
    elif isinstance(anything, (tuple, list)):
        return Geometry(*anything)
    else:
        return None

def _to_vertex(anything):
    if isinstance(anything, Vertex):
        return anything
    elif isinstance(anything, (tuple, list)):
        return Vertex(*anything)
    else:
        return None




class Color(Clutter.Color):
    def __init__(self, red=0, green=0, blue=0, alpha=0):
        Clutter.Color.__init__(self)
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __new__(cls, *args, **kwargs):
        return Clutter.Color.__new__(cls)

    def __repr__(self):
        return '<Clutter.Color(red=%d, green=%d, blue=%d, alpha=%s)>' % (
            self.red, self.green, self.blue, self.alpha)

    @classmethod
    def from_string(cls, color_string):
        color = Color()
        Clutter.Color.from_string(color, color_string)
        return color

Color = override(Color)
__all__.append('Color')


class ActorBox(Clutter.ActorBox):
    def __init__(self, x1=0.0, y1=0.0, x2=0.0, y2=0.0):
        Clutter.ActorBox.__init__(self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __new__(cls, *args, **kwargs):
        return Clutter.ActorBox.__new__(cls)

    def __repr__(self):
        return '<Clutter.ActorBox(x1=%f, y1=%f, x2=%f y2=%f)>' % (
            self.x1, self.y1, self.x2, self.y2)

ActorBox = override(ActorBox)
__all__.append('ActorBox')


class Vertex(Clutter.Vertex):
    def __new__(cls, *args, **kwargs):
        return Clutter.Vertex.__new__(cls)

    def __init__(self, x=0.0, y=0.0, z=0.0):
        Clutter.Vertex.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<Clutter.Vertex(x=%f, y=%f, z=%f)>' % (self.x, self.y, self.z)

Vertex = override(Vertex)
__all__.append('Vertex')


class Geometry(Clutter.Geometry):
    def __new__(cls, *args, **kwargs):
        return Clutter.Geometry.__new__(cls)

    def __init__(self, x=0, y=0, width=0, height=0):
        Clutter.Geometry.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return '<Clutter.Geometry(x=%d, y=%d, width=%d, height=%d)>' % (
            self.x, self.y, self.width, self.height)

Geometry = override(Geometry)
__all__.append('Geometry')


class Event(Clutter.Event):
    _UNION_MEMBERS = {
        Clutter.EventType.KEY_PRESS: 'key',
        Clutter.EventType.KEY_RELEASE: 'key',
        Clutter.EventType.MOTION: 'motion',
        Clutter.EventType.ENTER: 'crossing',
        Clutter.EventType.LEAVE: 'crossing',
        Clutter.EventType.BUTTON_PRESS: 'button',
        Clutter.EventType.BUTTON_RELEASE: 'button',
        Clutter.EventType.SCROLL: 'scroll',
        Clutter.EventType.STAGE_STATE: 'stage_state'
    }
    def __new__(cls, *args, **kwargs):
        return Clutter.Event.__new__(cls)

    def __getattr__(self, name):
        real_event = getattr(self, '_UNION_MEMBERS').get(self.type())
        if real_event:
            return getattr(getattr(self, real_event), name)
        else:
            return getattr(self, name)

Event = override(Event)
__all__.append('Event')




class Actor(Clutter.Actor):
    def _update_animation(self, *args):
        def _detach_animation(animation):
            delattr(self, '_animation')
            del animation
        if hasattr(self, '_animation'):
            animation = getattr(self, '_animation')
        else:
            animation = Clutter.Animation()
            animation.set_object(self)
            animation.connect('completed', _detach_animation)
            setattr(self, '_animation', animation)

        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Actor.animate requires at least one " +
                             "property/value pair")

        for prop, value in zip(args[::2], args[1::2]):
            if prop.startswith("fixed::"):
                prop = prop[7:]
                self.set_property(prop, value)
            elif animation.has_property(prop):
                animation.update(prop, value)
            else:
                animation.bind(prop, value)
        return animation

    def animate(self, mode, duration, *args):
        animation = self._update_animation(*args)
        animation.set_mode(mode)
        animation.set_duration(duration)
        animation.get_timeline().start()
        return animation

    def animate_with_timeline(self, mode, timeline, *args):
        animation = self._update_animation(*args)
        animation.set_mode(mode)
        animation.set_timeline(timeline)
        animation.get_timeline().start()
        return animation

    def animate_with_alpha(self, alpha, *args):
        animation = self._update_animation(*args)
        animation.set_alpha(alpha)
        animation.get_timeline().start()
        return animation

    def raise_actor(self, below):
        parent = self.get_parent()
        if not parent:
            return
        parent.raise_child(self, below)

    def lower_actor(self, above):
        parent = self.get_parent()
        if not parent:
            return
        parent.lower_child(self, above)


Actor = override(Actor)
__all__.append('Actor')


class Container(Clutter.Container):
    def __len__(self):
        return len(self.get_children())

    def __contains__(self, actor):
        return actor in self.get_children()

    def __iter__(self):
        return iter(self.get_children())

    def add(self, *actors):
        for actor in actors:
            Clutter.Container.add_actor(self, actor)

    def remove(self, *actors):
        for actor in actors:
            Clutter.Container.remove_actor(self, actor)

Container = override(Container)
__all__.append('Container')


class Stage(Clutter.Stage, Actor):
    def set_color(self, color):
        Clutter.Stage.set_color(self, _to_color(color))

Stage = override(Stage)
__all__.append('Stage')


class Texture(Clutter.Texture, Actor):
    def __init__(self, filename=None, **kwargs):
        Clutter.Texture.__init__(self, **kwargs)
        if filename:
            self.set_from_file(filename)

Texture = override(Texture)
__all__.append('Texture')


class Rectangle(Clutter.Rectangle, Actor):
    def __init__(self, color=None, **kwargs):
        Clutter.Rectangle.__init__(self, **kwargs)
        if color:
            self.set_color(color)

    def set_color(self, color):
        Clutter.Rectangle.set_color(self, _to_color(color))

    def set_border_color(self, color):
        Clutter.Rectangle.set_border_color(self, _to_color(color))

Rectangle = override(Rectangle)
__all__.append('Rectangle')


class Text(Clutter.Text, Actor):
    def __init__(self, font_name=None, text=None, color=None, **kwargs):
        Clutter.Text.__init__(self, **kwargs)
        if font_name:
            self.props.font_name = font_name
        if text:
            self.props.text = text
        if color:
            self.props.color = color

    def set_color(self, color):
        Clutter.Text.set_color(self, _to_color(color))

Text = override(Text)
__all__.append('Text')


class CairoTexture(Clutter.CairoTexture):
    def __init__(self, width, height, **kwargs):
        Clutter.CairoTexture.__init__(self, **kwargs)
        self.set_surface_size(width, height)

CairoTexture = override(CairoTexture)
__all__.append('CairoTexture')


class Clone(Clutter.Clone):
    def __init__(self, source=None, **kwargs):
        Clutter.Clone.__init__(self, **kwargs)
        if source:
            self.set_source(source)

Clone = override(Clone)
__all__.append('Clone')


class Box(Clutter.Box, Actor):
    def __init__(self, layout_manager=None, **kwargs):
        Clutter.Box.__init__(self, **kwargs)
        if layout_manager:
            self.set_layout_manager(layout_manager)

    def set_color(self, color):
        Clutter.Box.set_color(self, _to_color(color))

    def pack(self, actor, **kwargs):
        self.add_actor(actor)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(actor, k, v)

    def pack_after(self, actor, silbing, **kwargs):
        self.add_actor(actor)
        self.raise_child(actor, silbing)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(actor, k, v)

    def pack_before(self, actor, silbing, **kwargs):
        self.add_actor(actor)
        self.lower_child(actor, silbing)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(actor, k, v)

Box = override(Box)
__all__.append('Box')


class BinLayout(Clutter.BinLayout):
    def __init__(self,
                 x_align=Clutter.BinAlignment.CENTER,
                 y_align=Clutter.BinAlignment.CENTER):
        Clutter.BinLayout.__init__(self)
        self.props.x_align = x_align
        self.props.y_align = y_align

BinLayout = override(BinLayout)
__all__.append('BinLayout')



class FlowLayout(Clutter.FlowLayout):
    def __init__(self, orientation=Clutter.FlowOrientation.HORIZONTAL,
                 **kwargs):
        Clutter.FlowLayout.__init__(self, **kwargs)
        self.props.orientation = orientation

FlowLayout = override(FlowLayout)
__all__.append('FlowLayout')


class BindConstraint(Clutter.BindConstraint):
    def __init__(self, source, coordinate, offset):
        Clutter.BindConstraint.__init__(self)
        self.props.source = source
        self.props.coordinate = coordinate
        self.props.offset = offset

BindConstraint = override(BindConstraint)
__all__.append('BindConstraint')


class AlignConstraint(Clutter.AlignConstraint):
    def __init__(self, source, axis, factor):
        Clutter.AlignConstraint.__init__(self)
        self.props.source = source
        self.props.align_axis = axis
        self.props.factor = factor

AlignConstraint = override(AlignConstraint)
__all__.append('AlignConstraint')


# provide backwards compatibility to clutter 1.4
if hasattr(Clutter, 'SnapConstraint'):
    class SnapConstraint(Clutter.SnapConstraint):
        def __init__(self, source):
            Clutter.SnapConstraint.__init__(self)
            self.props.source = source

    SnapConstraint = override(SnapConstraint)
    __all__.append('SnapConstraint')

if hasattr(Clutter, 'PathConstraint'):
    class PathConstraint(Clutter.PathConstraint):
        def __init__(self, path, offset):
            Clutter.PathConstraint.__init__(self)
            self.props.path = path
            self.props.offset = offset

    PathConstraint = override(PathConstraint)
    __all__.append('PathConstraint')



class PageTurnEffect(Clutter.PageTurnEffect):
    def __init__(self, period, angle, radius):
        Clutter.PageTurnEffect.__init__(self)
        self.props.period = period
        self.props.angle = angle
        self.props.radius = radius

PageTurnEffect = override(PageTurnEffect)
__all__.append('PageTurnEffect')


class ColorizeEffect(Clutter.ColorizeEffect):
    def __init__(self, color):
        Clutter.ColorizeEffect.__init__(self)
        self.set_tint(color)

    def set_tint(self, color):
        Clutter.ColorizeEffect.set_tint(self, _to_color(color))

ColorizeEffect = override(ColorizeEffect)
__all__.append('ColorizeEffect')


class DesaturateEffect(Clutter.DesaturateEffect):
    def __init__(self, factor):
        Clutter.DesaturateEffect.__init__(self)
        self.props.factor = factor

DesaturateEffect = override(DesaturateEffect)
__all__.append('DesaturateEffect')




class Model(Clutter.Model):
    def insert(self, row, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.insert needs at least one " +
                             "column / value pair")
        for column, value in zip(args[::2], args[1::2]):
            self.insert_value(row, column, value)

    def append(self, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.append needs at least one " +
                             "column / value pair")
        row = self.get_n_rows()
        self.insert(row, *args)

    def prepend(self, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.prepend needs at least one " +
                             "column / value pair")
        # FIXME: This won't work
        self.insert(-1, *args)

Model = override(Model)
__all__.append('Model')


class ListModel(Clutter.ListModel):
    def __init__(self, *args):
        Clutter.ListModel.__init__(self)
        if len(args) < 2 or len(args) % 2:
            raise TypeError("Clutter.ListModel requires at least one " +
                            "type / name pair")
        self.set_types(args[::2])
        self.set_names(args[1::2])

ListModel = override(ListModel)
__all__.append('ListModel')



class Timeline(Clutter.Timeline):
    def __init__(self, duration=1000, **kwargs):
        Clutter.Timeline.__init__(self, **kwargs)
        self.set_duration(duration)

Timeline = override(Timeline)
__all__.append('Timeline')


class Alpha(Clutter.Alpha):
    def __init__(self, timeline=None, mode=0):
        Clutter.Alpha.__init__(self)
        if timeline:
            self.set_timeline(timeline)
        if mode:
            self.set_mode(mode)

Alpha = override(Alpha)
__all__.append('Alpha')


class BehaviourDepth(Clutter.BehaviourDepth):
    def __init__(self, alpha=None, depth_start=0, depth_end=0):
        Clutter.BehaviourDepth.__init__(self)
        self.props.alpha = alpha
        self.props.depth_start = depth_start
        self.props.depth_end = depth_end

BehaviourDepth = override(BehaviourDepth)
__all__.append('BehaviourDepth')


class BehaviourEllipse(Clutter.BehaviourEllipse):
    def __init__(self, alpha=None, x=0, y=0, width=0, height=0,
                 direction=Clutter.RotateDirection.CW,
                 start=0.0, end=0.0):
        Clutter.BehaviourEllipse.__init__(self)
        self.props.alpha = alpha
        self.props.x = x
        self.props.y = y
        self.props.width = width
        self.props.height = height
        self.props.direction = direction
        self.props.start = start
        self.props.end = end

BehaviourEllipse = override(BehaviourEllipse)
__all__.append('BehaviourEllipse')


class BehaviourOpacity(Clutter.BehaviourOpacity):
    def __init__(self, opacity_start=0, opacity_end=0, alpha=None):
        Clutter.BehaviourOpacity.__init__(self)
        self.props.opacity_start = opacity_start
        self.props.opacity_end = opacity_end
        self.props.alpha = alpha

BehaviourOpacity = override(BehaviourOpacity)
__all__.append('BehaviourOpacity')


class Path(Clutter.Path):
    def __init__(self, description=None):
        Clutter.Path.__init__(self)
        if description:
            self.set_description(description)

Path = override(Path)
__all__.append('Path')


class BehaviourPath(Clutter.BehaviourPath):
    def __init__(self, alpha=None, path=None, description=None):
        Clutter.BehaviourPath.__init__(self)
        self.props.alpha = alpha
        if path:
            self.set_path(path)
        elif description is not None:
            path = Path(description)
            self.set_path(path)

BehaviourPath = override(BehaviourPath)
__all__.append('BehaviourPath')


class BehaviourRotate(Clutter.BehaviourRotate):
    def __init__(self, alpha=None, axis=Clutter.RotateAxis.X_AXIS,
                 direction=Clutter.RotateDirection.CW,
                 angle_start=0.0, angle_end=0.0):
        Clutter.BehaviourRotate.__init__(self)
        self.props.alpha = alpha
        self.props.axis = axis
        self.props.direction = direction
        self.props.angle_start = angle_start
        self.props.angle_end = angle_end

BehaviourRotate = override(BehaviourRotate)
__all__.append('BehaviourRotate')


class BehaviourScale(Clutter.BehaviourScale):
    def __init__(self, alpha=None,
                 x_scale_start=1.0, x_scale_end=1.0,
                 y_scale_start=1.0, y_scale_end=1.0):
        Clutter.BehaviourScale.__init__(self)
        self.props.alpha = alpha
        self.props.x_scale_start = x_scale_start
        self.props.y_scale_start = y_scale_start
        self.props.x_scale_end = x_scale_end
        self.props.y_scale_end = y_scale_end

BehaviourScale = override(BehaviourScale)
__all__.append('BehaviourScale')



class Script(Clutter.Script):
    def get_objects(self, *objects):
        ret = []
        for name in objects:
            obj = self.get_object(name)
            ret.append(obj)
        return ret

Script = override(Script)
__all__.append('Script')


class BindingPool(Clutter.BindingPool):
    def __init__(self, name):
        Clutter.BindingPool.__init__(self)
        self.props.name = name

BindingPool = override(BindingPool)
__all__.append('BindingPool')


class Shader(Clutter.Shader):
    def set_vertex_source(self, data):
        Clutter.Shader.set_vertex_source(self, data, -1)

    def set_fragment_source(self, data):
        Clutter.Shader.set_fragment_source(self, data, -1)

Shader = override(Shader)
__all__.append('Shader')


# override the main_quit function to ignore additional arguments. This enables
# common stuff like stage.connect('destroy', Clutter.main_quit)
def main_quit(*args, **kwargs):
    Clutter.main_quit()

__all__.append('main_quit')


clutter_version = (Clutter.MAJOR_VERSION, Clutter.MINOR_VERSION,
                   Clutter.MICRO_VERSION)
__all__.append('clutter_version')


# Initialize Clutter directly on import
initialized, argv = Clutter.init(sys.argv)
sys.argv = argv
if not initialized:
    raise RuntimeError("Could not initialize Cluttter")
