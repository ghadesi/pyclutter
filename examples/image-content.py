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

    # Change the label
    text.props.text = 'Content Gravity: ' + gravities[current_gravity][1]

    # Animate the content gravity changes
    with actor.easing_state():
        actor.set_content_gravity(gravities[current_gravity][0])

    # Cycle through all gravities
    current_gravity += 1
    if current_gravity >= len(gravities):
        current_gravity = 0

if __name__ == '__main__':
    # Our stage
    stage = Clutter.Stage(title='Content Box', user_resizable=True)
    stage.set_margin(Clutter.Margin(12))
    stage.connect('destroy', Clutter.main_quit)
    stage.show()

    # Load the texture data from a file
    pixbuf = GdkPixbuf.Pixbuf.new_from_file('redhand.png')

    # Use the correct pixel format depending on whether the image
    # has an alpha channel
    pixel_format = Cogl.PixelFormat.RGB_888
    if pixbuf.get_has_alpha():
        pixel_format = Cogl.PixelFormat.RGBA_8888

    data = pixbuf.read_pixel_bytes()
    width = pixbuf.get_width()
    height = pixbuf.get_height()
    stride = pixbuf.get_rowstride()

    # The Image content knows how to draw texture data
    image = Clutter.Image()
    image.set_bytes(data, pixel_format, width, height, stride)

    # A Stage is like any other actor, and can paint a Content
    stage.set_content_gravity(Clutter.ContentGravity.RESIZE_ASPECT)
    stage.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR, Clutter.ScalingFilter.LINEAR)
    stage.set_content(image)

    # Show a label with the current content gravity
    label = 'Content Gravity: Resize Aspect'
    text = Clutter.Text(text=label)
    text.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(text)

    # Change the content gravity on tap/click
    action = Clutter.TapAction()
    action.connect('tap', on_tap, text)
    stage.add_action(action)

    Clutter.main()
