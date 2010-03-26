import random
import clutter
from clutter import cogl

class TestBoxLayout(object):
    def __init__(self):
        self.stage = clutter.Stage()
        self.stage.set_title("Box Layout")
        self.stage.set_size(640, 480)
        self.stage.set_user_resizable(True)
        self.stage.connect('destroy', clutter.main_quit)

        self.layout = clutter.BoxLayout()
        self.box = clutter.Box(self.layout)
        self.stage.add(self.box)

        self.stage.connect('key-press-event', self.on_key_press)
        self.stage.connect('allocation-changed', self.on_allocation_changed)

        self.last_index = 0
        self.expand = True
        self.hover_actor = None

        for i in range(5):
            self.add_actor()

    def on_key_press(self, stage, event):
        from clutter import keysyms
        if event.keyval == keysyms.a:
            toggle = self.layout.get_use_animations()
            self.layout.set_use_animations(not toggle)
        elif event.keyval == keysyms.v:
            toggle = self.layout.get_vertical()
            self.layout.set_vertical(not toggle)
        elif event.keyval == keysyms.p:
            toggle = self.layout.get_pack_start()
            self.layout.set_pack_start(not toggle)
        elif event.keyval == keysyms.s:
            spacing = self.layout.get_spacing()
            if spacing > 12:
                spacing = 0
            else:
                spacing += 1
            self.layout.set_spacing(spacing)
        elif event.keyval == keysyms.m:
            self.add_actor()
        elif event.keyval == keysyms.q:
            clutter.main_quit()
        else:
            return False
        return True

    def on_allocation_changed(self, stage, allocation, flags):
        width, height = allocation.size
        self.box.set_size(width - 100, height - 100)

    def add_actor(self):
        color = clutter.color_from_hls(random.randint(0, 360), 0.5, 0.5)
        color.alpha = 0xff
        rect = clutter.Rectangle()
        rect.set_color(color)
        rect.set_size(32, 64)
        self.layout.pack(rect, self.expand, False, False,
                         clutter.BOX_ALIGNMENT_CENTER,
                         clutter.BOX_ALIGNMENT_CENTER)
        rect.set_reactive(True)
        rect.connect_after('paint', self.on_paint, self.last_index)
        rect.connect('enter-event', self.on_enter)
        rect.connect('leave-event', self.on_leave)
        rect.connect('button-release-event', self.on_button_release)
        self.expand = not self.expand
        self.last_index += 1

    def on_paint(self, actor, index):
        text = "%d" % index
        box = clutter.ActorBox(*actor.get_allocation_box())
        width, height = box.size
        layout = actor.create_pango_layout(text)
        layout_width, layout_height = layout.get_size()
        color = clutter.Color(0, 0, 0, 255)
        cogl.pango_render_layout(layout,
                                 int((width - (layout_width / 1024)) / 2),
                                 int((height - (layout_height / 1024)) / 2),
                                 clutter.Color(0, 0, 0, 255), 0)

    def on_enter(self, actor, event):
        color = clutter.Color(0x0, 0x0, 0x0, 0xff)
        actor.set_border_width(2)
        actor.set_border_color(color)
        self.hover_actor = actor

    def on_leave(self, actor, event):
        actor.set_border_width(0)
        self.hover_actor = None

    def on_button_release(self, actor, event):
        if event.button == 1:
            x_fill, y_fill = self.layout.get_fill(actor)
            self.layout.set_fill(actor, not x_fill, not y_fill)
        else:
            x_align, y_align = self.layout.get_alignment(actor)
            if x_align < 2:
                x_align += 1
            else:
                x_align = 0
            if y_align < 2:
                y_align += 1
            else:
                y_align = 0
            self.layout.set_alignment(actor, x_align, y_align)
        return True

    def run(self):
        self.stage.show()
        clutter.main()

if __name__ == '__main__':
    box_test = TestBoxLayout()
    box_test.run()
