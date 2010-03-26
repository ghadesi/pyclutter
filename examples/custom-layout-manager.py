import random
from gobject import property
import clutter

class SimpleBoxLayout(clutter.LayoutManager):
    __gtype_name__ = 'SimpleBoxLayout'
    vertical = property(type=bool, default=False)
    spacing = property(type=int, default=0)
    def __init__(self, vertical=False, spacing=0):
        super(SimpleBoxLayout, self).__init__()
        self.vertical = vertical
        self.spacing = spacing
        self.connect('notify::vertical', self.on_property_changed)
        self.connect('notify::spacing', self.on_property_changed)

    def on_property_changed(self, layout, pspec):
        self.layout_changed()

    def do_get_preferred_width(self, container, for_height):
        min_w = nat_w = 0
        children = container.get_children()
        for child in children:
            if self.vertical:
                child_min, child_nat = child.get_preferred_width(for_height)
                min_w = max(min_w, child_min)
                nat_w = max(nat_w, child_nat)
            else:
                child_min, child_nat = child.get_preferred_width(-1)
                min_w += child_min
                nat_w += child_nat

        if len(children) > 1 and not self.vertical:
            min_w += self.spacing * (len(children) - 1)
            nat_w += self.spacing * (len(children) - 1)

        return (min_w, nat_w)

    def do_get_preferred_height(self, container, for_width):
        min_h = nat_h = 0
        children = container.get_children()
        for child in children:
            if self.vertical:
                child_min, child_nat = child.get_preferred_height(-1)
                min_h += child_min
                nat_h += child_nat
            else:
                child_min, child_nat = child.get_preferred_height(for_width)
                min_h = max(min_h, child_min)
                nat_h = max(nat_h, child_nat)

        if len(children) > 1 and self.vertical:
            min_h += self.spacing * (len(children) - 1)
            nat_h += self.spacing * (len(children) - 1)

        return (min_h, nat_h)

    def do_allocate(self, container, allocation, flags):
        children = container.get_children()
        child_x = child_y = 0
        for child in children:
            w, h = child.get_preferred_size()[2:]
            box = clutter.ActorBox()
            box.x1 = child_x
            box.y1 = child_y
            box.x2 = box.x1 + w
            box.y2 = box.y1 + h
            if self.vertical:
                child_y = box.y2 + self.spacing
            else:
                child_x = box.x2 + self.spacing
            child.allocate(box, flags)


if __name__ == '__main__':
    def on_key_press(stage, event):
        if event.keyval == clutter.keysyms.v:
            layout.props.vertical = not layout.props.vertical
            return True
        elif event.keyval == clutter.keysyms.s:
            spacing = layout.props.spacing
            if spacing > 20:
                spacing = 0
            else:
                spacing += 1
            layout.props.spacing = spacing
            return True

    stage = clutter.Stage()
    stage.connect('destroy', clutter.main_quit)
    stage.connect('key-press-event', on_key_press)

    layout = SimpleBoxLayout(True, 5)
    box = clutter.Box(layout)
    stage.add(box)

    for i in range(5):
        color = clutter.color_from_hls(random.randint(0, 360), 0.5, 0.5)
        color.alpha = 255
        rect = clutter.Rectangle(color)
        rect.set_size(50, 50)
        box.add(rect)

    stage.show()
    clutter.main()
