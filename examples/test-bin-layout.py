from random import randint

import cairo
import clutter
from clutter import cogl


class TestBinLayout(object):
    def __init__(self):
        self.bg_round_radius = 12
        stage_color = clutter.Color(0xe0, 0xf2, 0xfc, 0xff)
        bg_color = clutter.Color(0xcc, 0xcc, 0xcc, 0x99)
        self.stage = clutter.Stage()
        self.stage.set_title("Box test")
        self.stage.set_size(640, 480)
        self.stage.set_color(stage_color)
        self.stage.connect('destroy', clutter.main_quit)

        self.layout = clutter.BinLayout(clutter.BIN_ALIGNMENT_CENTER,
                                        clutter.BIN_ALIGNMENT_CENTER)
        self.box = clutter.Box(self.layout)
        self.stage.add(self.box)
        self.box.set_anchor_point_from_gravity(clutter.GRAVITY_CENTER)
        self.box.set_position(320, 240)
        self.box.set_reactive(True)
        self.box.set_name('box')

        rect = self.make_background(bg_color, 200, 200)
        self.box.pack(rect,
                      'x-align', clutter.BIN_ALIGNMENT_CENTER,
                      'y-align', clutter.BIN_ALIGNMENT_CENTER)
        rect.lower_bottom()
        rect.set_name('background')

        tex = clutter.Texture('redhand.png')
        tex.set_keep_aspect_ratio(True)
        self.layout.add(tex,
                        clutter.BIN_ALIGNMENT_CENTER,
                        clutter.BIN_ALIGNMENT_CENTER)
        tex.raise_actor(rect)
        tex.set_width(175)
        tex.set_name('texture')

        c = clutter.Color(randint(0, 255), randint(0, 255), randint(0, 255), 224)
        rect = clutter.Rectangle(c)
        self.box.add(rect)
        self.layout.set_alignment(rect,
                                  clutter.BIN_ALIGNMENT_END,
                                  clutter.BIN_ALIGNMENT_END)
        rect.set_size(50, 50)
        rect.set_opacity(0)
        rect.raise_top()
        rect.set_name('emblem')
        self.emblem = rect

        self.box.connect('enter-event', self.on_box_enter)
        self.box.connect('leave-event', self.on_box_leave)

    def make_background(self, color, width, height):
        x = y = 0
        r = self.bg_round_radius
        tex = clutter.CairoTexture(width, height)
        cr = tex.cairo_create()

        cr.move_to(r, y)
        cr.line_to(width - r, y)
        cr.curve_to(width, y, width, y, width, r)
        cr.line_to(width, height - r)
        cr.curve_to(width, height, width, height, width - r, height)
        cr.line_to(r, height)
        cr.curve_to(x, height, x, height, x, height - r)
        cr.line_to(x, r)
        cr.curve_to(x, y, x, y, r, y)
        cr.close_path()
        cr.stroke()

        x += 4
        y += 4
        width -= 4
        height -= 4

        cr.move_to(r, y)
        cr.line_to(width - r, y)
        cr.curve_to(width, y, width, y, width, r)
        cr.line_to(width, height - r)
        cr.curve_to(width, height, width, height, width - r, height)
        cr.line_to(r, height)
        cr.curve_to(x, height, x, height, x, height - r)
        cr.line_to(x, r)
        cr.curve_to(x, y, x, y, r, y)
        cr.close_path()

        pat = cairo.LinearGradient(0, 0, 0, height)
        pat.add_color_stop_rgba(1, .85, .85, .85, 1)
        pat.add_color_stop_rgba(.95, 1, 1, 1, 1)
        pat.add_color_stop_rgba(.05, 1, 1, 1, 1)
        pat.add_color_stop_rgba(0, .85, .85, .85, 1)

        cr.set_source(pat)
        cr.fill()

        del cr
        return tex

    def on_box_enter(self, box, event):
        self.emblem.animate(clutter.LINEAR, 150, 'opacity', 255)
        return True

    def on_box_leave(self, box, event):
        self.emblem.animate(clutter.LINEAR, 150, 'opacity', 0)
        return True

    def run(self):
        self.stage.show()
        clutter.main()


if __name__ == '__main__':
    test_box = TestBinLayout()
    test_box.run()
