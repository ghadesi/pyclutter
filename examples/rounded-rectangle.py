import math
import cairo
from gi.repository import GObject
from gi.repository import Clutter

def draw_content(canvas, cr, surface_width, surface_height):
    padding = 2
    x = padding
    y = padding
    width = surface_width - (padding * 2)
    height = surface_height - (padding * 2)
    aspect = 1.0
    corner_radius = height / 20.0
    radius = corner_radius / aspect
    degrees = math.pi / 180

    cr.save()
    cr.set_operator(cairo.OPERATOR_CLEAR)
    cr.paint()
    cr.restore()

    cr.new_sub_path()
    cr.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
    cr.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
    cr.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)
    cr.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
    cr.close_path()

    cr.set_source_rgb(0.5, 0.5, 1)
    cr.fill()

    return True

if __name__ == '__main__':
    stage = Clutter.Stage()
    stage.props.title = 'Rounded Rectangle'
    stage.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.BLACK)
    stage.set_size(500, 500)
    stage.show()

    canvas = Clutter.Canvas(width=300, height=300)

    actor = Clutter.Actor(content=canvas,
                          content_gravity=Clutter.ContentGravity.CENTER,
                          request_mode=Clutter.RequestMode.CONTENT_SIZE)
    actor.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR, Clutter.ScalingFilter.LINEAR)
    actor.set_pivot_point(0.5, 0.5)
    actor.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(actor)

    transition = Clutter.PropertyTransition('rotation-angle-y')
    transition.set_from(0)
    transition.set_to(360)
    transition.set_duration(2000)
    transition.set_repeat_count(-1)
    actor.add_transition('rotateActor', transition)

    stage.connect('destroy', Clutter.main_quit)

    canvas.connect('draw', draw_content)
    canvas.invalidate()

    Clutter.main()
