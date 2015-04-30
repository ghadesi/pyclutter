import math
import cairo

from gi.repository import GLib
from gi.repository import Clutter

resize_id = 0

def draw_clock(canvas, cr, width, height):
    # Clear the canvas
    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.paint()
    cr.restore()

    # Get the current time, and compute the angles
    now = GLib.DateTime.new_now_local()
    seconds = now.get_second() * math.pi / 30
    minutes = now.get_minute() * math.pi / 30
    hours = now.get_hour() * math.pi / 6

    # Normalize the coordinate space 
    cr.scale(width, height)

    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(0.1)

    # The black rail that holds the seconds indicator
    color = Clutter.Color.get_static(Clutter.StaticColor.BLACK)
    Clutter.cairo_set_source_color(cr, color)
    cr.translate(0.5, 0.5)
    cr.arc(0, 0, 0.4, 0, math.pi * 2)
    cr.stroke()

    # The seconds indicator
    color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)
    color.alpha = 196
    Clutter.cairo_set_source_color(cr, color)
    cr.move_to(0, 0)
    cr.arc(math.sin(seconds) * 0.4, - math.cos(seconds) * 0.4, 0.05, 0, math.pi * 2)
    cr.fill()

    # The minutes hand
    color = Clutter.Color.get_static(Clutter.StaticColor.CHAMELEON_DARK)
    color.alpha = 196
    Clutter.cairo_set_source_color(cr, color)
    cr.move_to(0, 0)
    cr.line_to(math.sin(minutes) * 0.4, - math.cos(minutes) * 0.4)
    cr.stroke()

    # The hours hand
    cr.move_to(0, 0)
    cr.line_to(math.sin(hours) * 0.2, - math.cos(hours) * 0.2)
    cr.stroke()

    return True

def invalidate_clock(canvas):
    canvas.invalidate()
    return True

def idle_resize(actor):
    global resize_id

    # Match the size of the canvas with the size of the actor
    width, height = actor.get_size()
    actor.get_content().set_size(math.ceil(width), math.ceil(height))

    resize_id = 0

    return False

def on_actor_resize(actor, allocation, flags):
    global resize_id

    # Throttle multiple allocations to a single canvas resize
    if resize_id == 0:
        resize_id = GLib.timeout_add(500, idle_resize, actor)

if __name__ == '__main__':
    Clutter.init(None)

    # Our stage
    stage = Clutter.Stage(title='2D Clock', user_resizable=True)
    stage.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.SKY_BLUE_LIGHT)
    stage.set_size(300, 300)
    stage.connect('destroy', Clutter.main_quit)
    stage.show()

    # The canvas, courtesy of Cairo
    canvas = Clutter.Canvas(width=300, height=300)
    canvas.connect('draw', draw_clock)
    canvas.invalidate()

    # The actor that displays the canvas
    actor = Clutter.Actor(content=canvas)
    actor.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR,
                                      Clutter.ScalingFilter.LINEAR)
    actor.add_constraint(Clutter.BindConstraint(source=stage, coordinate=Clutter.BindCoordinate.SIZE))
    actor.connect('allocation-changed', on_actor_resize)
    stage.add_child(actor)

    # Set up a timeout that invalidates the contents of the canvas every second
    GLib.timeout_add(1000, invalidate_clock, canvas)

    Clutter.main()
