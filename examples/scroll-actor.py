from gi.repository import Clutter

class MenuItem(Clutter.Text):
    def __init__(self, label=''):
        Clutter.Text.__init__(self)
        self.props.font_name = 'Sans Bold 24'
        self.props.text = label
        self.props.color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)
        self.props.margin_left = 12
        self.props.margin_right = 12

class Menu(Clutter.Actor):
    def __init__(self):
        Clutter.Actor.__init__(self)

        layout = Clutter.BoxLayout(orientation=Clutter.Orientation.VERTICAL, spacing=12)
        self.props.layout_manager = layout
        self.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.BLACK)

        self._current_idx = 0

    def select_next(self):
        old_item = self.get_child_at_index(self._current_idx)
        old_item.props.color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)

        self._current_idx += 1

        if self._current_idx == self.get_n_children():
            self._current_idx = 0

        new_item = self.get_child_at_index(self._current_idx)
        new_item.props.color = Clutter.Color.get_static(Clutter.StaticColor.SKY_BLUE_LIGHT)
        return new_item

    def select_prev(self):
        old_item = self.get_child_at_index(self._current_idx)
        old_item.props.color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)

        self._current_idx -= 1

        if self._current_idx < 0:
            self._current_idx = self.get_n_children() - 1;

        new_item = self.get_child_at_index(self._current_idx)
        new_item.props.color = Clutter.Color.get_static(Clutter.StaticColor.SKY_BLUE_LIGHT)
        return new_item

def create_menu_actor(scroll):
    menu = Menu()
    scroll.add_child(menu)

    menu_items = [
        'Option 1',
        'Option 2',
        'Option 3',
        'Option 4',
        'Option 5',
        'Option 6',
        'Option 7',
        'Option 8',
        'Option 9',
        'Option 10',
        'Option 11',
        'Option 12'
    ]

    for label in menu_items:
        menu.add_child(MenuItem(label))

def create_scroll_actor(stage):
    scroll = Clutter.ScrollActor(name='scroll')
    scroll.set_position(0, 18)
    scroll.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.X_AXIS, factor=0.5))
    scroll.add_constraint(Clutter.BindConstraint(source=stage, coordinate=Clutter.BindCoordinate.HEIGHT, offset=-36))
    scroll.set_scroll_mode(Clutter.ScrollMode.VERTICALLY)
    scroll.set_easing_duration(250)

    create_menu_actor(scroll)

    stage.add_child(scroll)

def scroll_to_item(scroll, item):
    pos = Clutter.Point()
    pos.x, pos.y = item.get_position()
    scroll.scroll_to_point(pos)

def select_prev_item(scroll):
    menu = scroll.get_first_child()
    item = menu.select_prev()
    scroll_to_item(scroll, item)

def select_next_item(scroll):
    menu = scroll.get_first_child()
    item = menu.select_next()
    scroll_to_item(scroll, item)

def on_key_press(stage, event):
    scroll = stage.get_first_child()
    key = event.keyval

    if key == Clutter.KEY_q:
        Clutter.main_quit()
        return True

    if key == Clutter.KEY_Up:
        select_prev_item(scroll)
        return True

    if key == Clutter.KEY_Down:
        select_next_item(scroll)
        return True

    return False

if __name__ == '__main__':
    Clutter.init(None)

    stage = Clutter.Stage(title='Scroll Actor', user_resizable=True)
    stage.connect('destroy', Clutter.main_quit)
    stage.connect('key-press-event', on_key_press)
    stage.show()

    create_scroll_actor(stage)

    Clutter.main()
