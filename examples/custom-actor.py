import sys
import gobject
import clutter

from clutter import cogl

class Triangle (clutter.Actor):
    """
    Triangle (clutter.Actor)

    A simple actor drawing a triangle using the clutter.cogl primitives
    """
    __gtype_name__ = 'Triangle'
    __gproperties__ = {
      'color' : ( \
        str, 'color', 'Color', None, gobject.PARAM_READWRITE \
      ),
    }
    __gsignals__ = {
        'clicked' : ( \
          gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, () \
        ),
    }

    def __init__ (self):
        clutter.Actor.__init__(self)
        self._color = clutter.color_parse('White')
        self._is_pressed = False
        self.connect('button-press-event', self.do_button_press_event)
        self.connect('button-release-event', self.do_button_release_event)
        self.connect('leave-event', self.do_leave_event)

    def set_color (self, color):
        self._color = clutter.color_parse(color)

    def do_set_property (self, pspec, value):
        if pspec.name == 'color':
            self._color = clutter.color_parse(value)
        else:
            raise TypeError('Unknown property ' + pspec.name)

    def do_get_property (self, pspec):
        if pspec.name == 'color':
            return self._color
        else:
            raise TypeError('Unknown property ' + pspec.name)

    def do_button_press_event (self, actor, event):
        if event.button == 1:
            self._is_pressed = True
            clutter.grab_pointer(self)
            return True
        else:
            return False

    def do_button_release_event (self, actor, event):
        if event.button == 1 and self._is_pressed == True:
            self._is_pressed = False
            clutter.ungrab_pointer()
            self.emit('clicked')
            return True
        else:
            return False

    def do_leave_event (self, actor, event):
        if self._is_pressed == True:
            self._is_pressed = False
            clutter.ungrab_pointer()
            return True
        else:
            return False

    def __paint_triangle (self, width, height, color):
        cogl.path_move_to(float(width / 2), 0)
        cogl.path_line_to(width, height)
        cogl.path_line_to(0, height)
        cogl.path_line_to(float(width / 2), 0)
        cogl.path_close()

        cogl.color(color)
        cogl.path_fill()

    def do_paint (self):
        (x, y, width, height) = self.get_allocation_geometry()

        paint_color = self._color

        real_alpha = self.get_paint_opacity() * paint_color.alpha / 255
        paint_color.alpha = real_alpha

        self.__paint_triangle(width, height, paint_color)

    def do_pick (self, pick_color):
        if self.should_pick_paint() == False:
            return

        (x, y, width, height) = self.get_allocation_geometry()
        self.__paint_triangle(width, height, pick_color)

    def do_clicked (self):
        sys.stdout.write("Clicked!\n")

gobject.type_register(Triangle)

if __name__ == '__main__':
    stage = clutter.Stage()
    stage.set_size(640, 480)
    stage.set_color(clutter.color_parse('Black'))
    stage.connect('destroy', clutter.main_quit)

    triangle = Triangle()
    triangle.set_color('Red')
    triangle.set_reactive(True)
    triangle.set_size(200, 200)
    triangle.set_anchor_point(100, 100)
    triangle.set_position(320, 240)
    stage.add(triangle)
    triangle.connect('clicked', clutter.main_quit)

    label = clutter.Label()
    label.set_font_name('Sans 36px')
    label.set_text('Click me!')
    label.set_color(clutter.color_parse('Red'))
    label.set_position((640 - label.get_width()) / 2, triangle.get_y() + triangle.get_height())
    stage.add(label)

    stage.show()

    clutter.main()

    sys.exit(0)