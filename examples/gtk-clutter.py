import sys

import cluttergtk   # must be the first to be imported
import clutter
import gtk

def main ():
    window = gtk.Window()
    window.connect('destroy', gtk.main_quit)
    window.set_title('cluttergtk.Embed')

    vbox = gtk.VBox(False, 6)
    window.add(vbox)

    embed = cluttergtk.Embed()
    embed.set_size_request(300, 300)
    vbox.pack_start(embed, True, False, 0)

    # we need to realize the widget before we get the stage
    embed.realize()

    stage = embed.get_stage()
    stage.set_color(clutter.color_parse('DarkBlue'))

    rect = clutter.Rectangle()
    rect.set_color(cluttergtk.get_base_color(window, gtk.STATE_SELECTED))
    rect.set_size(100, 100)
    rect.set_anchor_point(50, 50)
    rect.set_position(150, 150)
    rect.set_rotation(clutter.X_AXIS, 45.0, 0, 0, 0)
    stage.add(rect)

    tex = cluttergtk.Texture()
    tex.set_from_stock(embed, 'gtk-refresh', gtk.ICON_SIZE_DIALOG)
    tex.set_size(100, 100)
    tex.set_anchor_point(50, 50)
    tex.set_position(150, 150)
    tex.set_rotation(clutter.Z_AXIS, 60.0, 0, 0, 0)
    stage.add(tex)

    button = gtk.Button('Click me to quit')
    button.connect('clicked', gtk.main_quit)
    vbox.pack_end(button, False, False, 0)
    button.show()

    button = gtk.Button('gtk-ok')
    button.set_use_stock(True)
    vbox.pack_end(button, False, False, 0)
    button.show()

    window.show_all()

    gtk.main()

    return 0

if __name__ == '__main__':
    sys.exit(main())