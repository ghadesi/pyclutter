import sys

try:
    from gi.repository import GtkClutter
except ImportError:
    print('GtkClutter introspection data is not installed.')
    sys.exit(1)

from gi.repository import Clutter
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

class StyledEmbed(GtkClutter.Embed):
    """
    A GtkClutterEmbed class that uses the same style of the
    top-level window to draw its background.
    """
    def __init__(self):
        GtkClutter.Embed.__init__(self)

        self.connect('realize', self.on_realize)
        self.connect('size-allocate', self.on_size_allocate)
        self.connect('style-updated', self.on_style_changed)

        self._canvas = Clutter.Canvas(width=200, height=200)
        self._canvas.connect('draw', self.on_canvas_draw)

    def on_realize(self, widget):
        """
        Assign the Canvas content on realization.
        """
        stage = self.get_stage()
        stage.props.content = self._canvas

    def on_size_allocate(self, widget, alloc):
        """
        Resize the Canvas when the widget receives a new size.
        """
        self._canvas.set_size(alloc.width, alloc.height)

    def on_style_changed(self, widget):
        """
        Invalidate the content of the Canvas when the style
        changes.
        """
        self._canvas.invalidate()

    def on_canvas_draw(self, canvas, cr, width, height):
        # We proxy the style of the top-level; if we wanted to style the
        # GtkClutterEmbed widget directly we'd need a custom CSS style
        # provider and a style class
        style = self.get_toplevel().get_style_context()
        Gtk.render_background(style, cr, 0, 0, width, height)
        return True

class StyledButton(Clutter.Actor):
    def __init__(self, widget):
        Clutter.Actor.__init__(self)

        self.props.reactive = True

        self._widget = widget
        self._context = widget.get_style_context()

        self._canvas = Clutter.Canvas(width=100, height=100)
        self._canvas.connect('draw', self._on_canvas_draw)
        self.props.content = self._canvas
        self.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR, Clutter.ScalingFilter.LINEAR)

        action = Clutter.ClickAction()
        action.connect('clicked', self._on_clicked)
        self.add_action(action)

        self._crossing = False

    @GObject.Signal
    def clicked(self):
        pass

    def _on_clicked(self, action, actor):
        self.emit('clicked')

    def do_enter_event(self, event):
        self._crossing = True
        self._canvas.invalidate()
        return False

    def do_leave_event(self, event):
        self._crossing = False
        self._canvas.invalidate()
        return False

    def do_allocate(self, allocation, flags):
        self.set_allocation(allocation, flags)

        width, height = allocation.get_size()
        self._canvas.set_size(width, height)

    def _on_canvas_draw(self, canvas, cr, width, height):
        self._context.save()
        self._context.add_class('button')

        state = self._context.get_state()
        if self._crossing:
            state |= Gtk.StateFlags.PRELIGHT

        self._context.set_state(state)

        Gtk.render_background(self._context, cr, 0, 0, width, height)
        Gtk.render_frame(self._context, cr, 0, 0, width, height)
        self._context.restore()
        return True

def on_button_clicked(actor):
    print('Clicked!')

if __name__ == '__main__':
    GtkClutter.init(None)

    # Our top-level window
    window = Gtk.Window(title='Test')
    window.connect('destroy', Gtk.main_quit)
    window.show()

    # The styled GtkClutterEmbed widget
    embed = StyledEmbed()
    # Keep the size of the stage tied to the size of the embedding widget
    embed.props.use_layout_size = True
    window.add(embed)
    embed.show()

    stage = embed.get_stage()

    # A simple rectangle centered on the stage
    rect = StyledButton(window)
    rect.set_pivot_point(0.5, 0.5)
    rect.set_size(100, 100)
    rect.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    rect.connect('clicked', on_button_clicked)
    stage.add_child(rect)

    transition = Clutter.PropertyTransition(property_name='rotation-angle-y')
    transition.set_duration(2000)
    transition.set_from(0)
    transition.set_to(360)
    transition.set_repeat_count(-1)
    rect.add_transition('spin', transition)

    Gtk.main()
