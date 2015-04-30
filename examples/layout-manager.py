import math

from gi.repository import GObject
from gi.repository import Clutter

class MultiLayout(Clutter.LayoutManager):
    GRID = 0
    CIRCLE = 1

    def __init__(self):
        Clutter.LayoutManager.__init__(self)
        self._state = MultiLayout.GRID
        self._spacing = 0
        self._cell_width = -1
        self._cell_height = -1

    @GObject.Property(type=int)
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state != value:
            self._state = value
            self.layout_changed()

    @GObject.Property(type=int)
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        if self._spacing != value:
            self._spacing = value
            self.layout_changed()

    def do_get_preferred_width(self, actor, for_height):
        minimum = 0
        natural = 0
        max_natural = 0
        n_children = 0

        for child in actor:
            if not child.props.visible:
                continue

            min_w, nat_w = child.get_preferred_width(-1)
            max_natural = max(max_natural, nat_w)

            if self._state == MultiLayout.GRID:
                minimum += min_w
                natural += nat_w
            elif self._state == MultiLayout.CIRCLE:
                minimum = max(minimum, min_w)
                natural = max(natural, nat_w)

            n_children += 1

        self._cell_width = max_natural

        minimum += (self._spacing * (n_children - 1))
        natural += (self._spacing * (n_children - 1))

        return (minimum, natural)

    def do_get_preferred_height(self, actor, for_width):
        minimum = 0
        natural = 0
        max_natural = 0
        n_children = 0

        for child in actor:
            if not child.props.visible:
                continue

            min_h, nat_h = child.get_preferred_height(-1)
            max_natural = max(max_natural, nat_h)

            if self._state == MultiLayout.GRID:
                minimum += min_h
                natural += nat_h
            elif self._state == MultiLayout.CIRCLE:
                minimum = max(minimum, min_h)
                natural = max(natural, nat_h)

            n_children += 1

        self._cell_height = max_natural

        minimum += (self._spacing * (n_children - 1))
        natural += (self._spacing * (n_children - 1))

        return (minimum, natural)

    def _get_items_per_row(self, for_width):
        if for_width < 0:
            return 1

        if self._cell_width <= 0:
            return 1

        n_columns = int((for_width + self._spacing) / (self._cell_width + self._spacing))

        return max(n_columns, 1)

    def do_allocate(self, actor, allocation, flags):
        def get_visible_children(actor):
            n_visible_children = 0
            for child in actor:
                if not child.props.visible:
                    continue
                n_visible_children += 1

            return n_visible_children

        n_items = get_visible_children(actor)
        if n_items == 0:
            return

        x_offset, y_offset = allocation.get_origin()
        avail_width, avail_height = allocation.get_size()

        self.do_get_preferred_width(actor, avail_width)
        self.do_get_preferred_height(actor, avail_height)

        item_index = 0
        n_items_per_row = 0
        center = Clutter.Point()
        radius = 0
        if self._state == MultiLayout.GRID:
            n_items_per_row = self._get_items_per_row(avail_width)
            item_x = x_offset
            item_y = y_offset
        elif self._state == MultiLayout.CIRCLE:
            radius = min((avail_width - self._cell_width) / 2, (avail_height - self._cell_height) / 2)
            center.x = allocation.x2 / 2
            center.y = allocation.y2 / 2

        for child in actor:
            child_alloc = Clutter.ActorBox()

            if self._state == MultiLayout.GRID:
                if item_index == n_items_per_row:
                    item_index = 0
                    item_x = x_offset
                    item_y += self._cell_height + self._spacing

                child_alloc.x1 = item_x
                child_alloc.y1 = item_y
                item_x += self._cell_width + self._spacing
            elif self._state == MultiLayout.CIRCLE:
                theta = 2.0 * math.pi / n_items * item_index
                child_alloc.x1 = center.x + radius * math.sin(theta) - (self._cell_width / 2)
                child_alloc.y1 = center.y + radius * math.cos(theta) - (self._cell_height / 2)

            child_alloc.x2 = child_alloc.x1 + self._cell_width
            child_alloc.y2 = child_alloc.y1 + self._cell_height

            child.allocate(child_alloc, flags)

            item_index += 1

def on_enter(actor, event):
    actor.set_scale(1.2, 1.2)
    return True

def on_leave(actor, event):
    actor.set_scale(1.0, 1.0)
    return True

def on_key_press(stage, event, layout):
    key = event.keyval
    if key == Clutter.KEY_q:
        Clutter.main_quit()
        return True

    if key == Clutter.KEY_t:
        if layout.state == MultiLayout.GRID:
            layout.state = MultiLayout.CIRCLE
        elif layout.state == MultiLayout.CIRCLE:
            layout.state = MultiLayout.GRID
        return True

    return False

if __name__ == '__main__':
    Clutter.init(None)

    stage = Clutter.Stage()
    stage.props.title = 'Multi-layout'
    stage.connect('destroy', Clutter.main_quit)
    stage.show()

    N_RECTS = 16
    RECT_SIZE = 64
    N_ROWS = 4
    PADDING = 12
    BOX_SIZE = (RECT_SIZE * (N_RECTS / N_ROWS) + PADDING * (N_RECTS / N_ROWS - 1))

    layout = MultiLayout()
    layout.spacing = PADDING
    box = Clutter.Actor(layout_manager=layout, width=BOX_SIZE, height=BOX_SIZE)
    box.set_margin(Clutter.Margin(PADDING))
    box.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(box)

    for i in range(N_RECTS):
        color = Clutter.Color.from_hls(360 / N_RECTS * i, 0.5, 0.8)
        color.alpha = 128 + 128 / N_RECTS * i

        rect = Clutter.Actor()
        rect.props.background_color = color
        rect.props.opacity = 0
        rect.props.reactive = True
        rect.set_size(RECT_SIZE, RECT_SIZE)
        rect.set_pivot_point(0.5, 0.5)
        rect.set_easing_duration(250)
        rect.set_easing_mode(Clutter.AnimationMode.EASE_OUT_CUBIC)
        box.add_child(rect)

        transition = Clutter.PropertyTransition(property_name='opacity', duration=250, delay=i*50)
        transition.set_from(0)
        transition.set_to(color.alpha)
        rect.add_transition('fadeIn', transition)

        rect.connect('enter-event', on_enter)
        rect.connect('leave-event', on_leave)

    label = Clutter.Text(text="Press t → Toggle layout\nPress q → Quit")
    label.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.X_AXIS, factor=0.50))
    label.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.Y_AXIS, factor=0.95))
    stage.add_child(label)

    stage.connect('key-press-event', on_key_press, layout)

    Clutter.main()
