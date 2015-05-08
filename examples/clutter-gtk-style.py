import sys

try:
    from gi.repository import GtkClutter
except ImportError:
    print('GtkClutter introspection data is not installed.')
    sys.exit(1)

from gi.repository import Clutter
from gi.repository import GLib
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
    rect = Clutter.Actor(background_color=Clutter.Color.get_static(Clutter.StaticColor.RED))
    rect.set_size(100, 100)
    rect.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(rect)

    Gtk.main()
