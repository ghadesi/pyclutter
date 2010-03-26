import random
import optparse

import clutter
from clutter import cogl

class TestFlowLayout(object):
    def __init__(self, n_rects, vertical, homogeneous, x_spacing, y_spacing,
                 random_size, fit_to_stage):
        self.n_rects = n_rects
        self.vertical = vertical
        self.homogeneous = homogeneous
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.fit_to_stage = fit_to_stage

        self.stage = clutter.Stage()
        self.stage.set_name("Flow Layout")
        self.stage.set_color(clutter.Color(0xe0, 0xf2, 0xfc, 0xff))
        self.stage.set_user_resizable(True)
        self.stage.connect('destroy', clutter.main_quit)
        self.stage.connect('allocation-changed', self.on_stage_resize)

        self.layout = clutter.FlowLayout(clutter.FLOW_HORIZONTAL)
        self.layout.set_homogeneous(True)
        self.layout.set_column_spacing(x_spacing)
        self.layout.set_row_spacing(y_spacing)

        self.box = clutter.Box(self.layout)
        self.box.set_color(clutter.Color(255, 255, 255, 255))
        self.box.set_name('box')
        self.stage.add(self.box)

        # setup rectangles
        for i in range(n_rects):
            color = clutter.color_from_hls(360. / n_rects * i, 0.5, 0.5)
            color.alpha = 224

            rect = clutter.Rectangle(color)
            if random_size:
                width = random.randint(50, 100)
                height = random.randint(50, 100)
            else:
                width = height = 50
            rect.set_size(width, height)
            self.box.add(rect)

    def on_stage_resize(self, actor, allocation, flags):
        if not self.fit_to_stage:
            return
        width, height = allocation.size
        if self.vertical:
            self.box.set_height(height)
        else:
            self.box.set_width(width)

    def run(self):
        self.stage.show()
        clutter.main()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-r', '--random-size', action='store_true',
                      help='Randomly size the rectangles')
    parser.add_option('-n', '--num-rects', type='int', default=20,
                      help='Number of rectangles')
    parser.add_option('-v', '--vertical', action='store_true',
                      help='Set vertical orientation')
    parser.add_option('--homogeneous', action='store_true',
                      help='Whether the layout should be homogeneous')
    parser.add_option('--x-spacing', type='int', default=0,
                      help='Horizontal spacing between elements')
    parser.add_option('--y-spacing', type='int', default=0,
                      help='Vertical spacing between elements')
    parser.add_option('--fit-to-stage', action='store_true',
                      help='Fit to the stage size')
    opts, args = parser.parse_args()

    test_box = TestFlowLayout(opts.num_rects, opts.vertical, opts.homogeneous,
                              opts.x_spacing, opts.y_spacing,
                              opts.random_size, opts.fit_to_stage)
    test_box.run()
