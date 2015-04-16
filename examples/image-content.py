# Clutter depends on Cogl 1.0 for public API, but Cogl ships with
# introspection data for both 1.0 and 2.0; pygobject will prefer
# the latter, so we need to explicitly version the Cogl module
# before loading it
import gi
gi.require_version('Cogl', '1.0')

from gi.repository import Cogl
from gi.repository import Clutter
from gi.repository import GdkPixbuf

gravities = [
    ( Clutter.ContentGravity.TOP_LEFT, 'Top Left' ),
    ( Clutter.ContentGravity.TOP, 'Top' ),
    ( Clutter.ContentGravity.TOP_RIGHT, 'Top Right' ),

    ( Clutter.ContentGravity.LEFT, 'Left' ),
    ( Clutter.ContentGravity.CENTER, 'Center' ),
    ( Clutter.ContentGravity.RIGHT, 'Right' ),

    ( Clutter.ContentGravity.BOTTOM_LEFT, 'Bottom Left' ),
    ( Clutter.ContentGravity.BOTTOM, 'Bottom' ),
    ( Clutter.ContentGravity.BOTTOM_RIGHT, 'Bottom Right' ),

    ( Clutter.ContentGravity.RESIZE_FILL, 'Resize Fill' ),
    ( Clutter.ContentGravity.RESIZE_ASPECT, 'Resize Aspect' )
]

current_gravity = 0

def on_tap(action, actor, text):
    global gravities, current_gravity

    with actor.easing_state():
        actor.set_content_gravity(gravities[current_gravity][0])

    text.props.text = 'Content Gravity: ' + gravities[current_gravity][1]

    current_gravity += 1
    if current_gravity >= len(gravities):
        current_gravity = 0

if __name__ == '__main__':
    stage = Clutter.Stage(title='Content Box', user_resizable=True)
    stage.set_margin(Clutter.Margin(12))
    stage.connect('destroy', Clutter.main_quit)
    stage.show()

    pixbuf = GdkPixbuf.Pixbuf.new_from_file('redhand.png')

    pixel_format = Cogl.PixelFormat.RGB_888
    if pixbuf.get_has_alpha():
        pixel_format = Cogl.PixelFormat.RGBA_8888

    width = pixbuf.get_width()
    height = pixbuf.get_height()
    stride = pixbuf.get_rowstride()

    image = Clutter.Image()
    image.set_bytes(pixbuf.read_pixel_bytes(), pixel_format, width, height, stride)

    stage.set_content_gravity(Clutter.ContentGravity.RESIZE_ASPECT)
    stage.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR,
                                      Clutter.ScalingFilter.LINEAR)
    stage.set_content(image)

    label = 'Content Gravity: Resize Aspect'
    text = Clutter.Text(text=label)
    text.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(text)

    action = Clutter.TapAction()
    action.connect('tap', on_tap, text)
    stage.add_action(action)

    Clutter.main()
