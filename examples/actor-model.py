from gi.repository import Clutter
from gi.repository import GObject
from gi.repository import Gio

class MenuItemModel(GObject.GObject):
    def __init__(self):
        GObject.GObject.__init__(self)

    label = GObject.Property(type=str, default='')
    selected = GObject.Property(type=bool, default=False)

class MenuItemView(Clutter.Text):
    def __init__(self):
        Clutter.Text.__init__(self)

        self._selected = False

        self.props.font_name = 'Sans Bold 24px'
        self.props.color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)
        self.props.margin_left = 12
        self.props.margin_right = 12

        self.set_pivot_point(0.5, 0.5)

        group = Clutter.TransitionGroup(duration=250, progress_mode=Clutter.AnimationMode.EASE_OUT)

        trans = Clutter.PropertyTransition(property_name='scale-x')
        trans.set_from(1.0)
        trans.set_to(3.0)
        group.add_transition(trans)

        trans = Clutter.PropertyTransition(property_name='scale-y')
        trans.set_from(1.0)
        trans.set_to(3.0)
        group.add_transition(trans)

        trans = Clutter.PropertyTransition(property_name='opacity')
        trans.set_from(255)
        trans.set_to(0)
        group.add_transition(trans)

        self.add_transition('activateTransition', group)
        group.stop()

        self.connect('transition-stopped', self._on_transition_stopped)

    def _on_transition_stopped(self, actor, transition, is_finished):
        if transition == 'activateTransition':
            self.set_scale(1, 1)
            self.set_opacity(255)

    def set_selected(self, value):
        self._selected = value
        if self._selected:
            self.props.color = Clutter.Color.get_static(Clutter.StaticColor.WHITE)
        else:
            self.props.color = Clutter.Color.get_static(Clutter.StaticColor.SKY_BLUE_LIGHT)

    def get_selected(self):
        return self._selected

    selected = GObject.Property(type=bool, default=False, setter=set_selected, getter=get_selected)

    def activate(self):
        self.get_transition('activateTransition').start()

class Menu(Clutter.Actor):
    def __init__(self):
        Clutter.Actor.__init__(self)

        layout = Clutter.BoxLayout(orientation=Clutter.Orientation.VERTICAL, spacing=12)
        self.props.layout_manager = layout

        self.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.BLACK)

        self._current_idx = -1

        def create_menu_item_view(item):
            view = MenuItemView()
            item.bind_property('label', view, 'text', GObject.BindingFlags.SYNC_CREATE)
            item.bind_property('selected', view, 'selected', GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)
            return view

        self._model = Gio.ListStore(item_type=MenuItemModel)
        self.bind_model(self._model, create_menu_item_view)

    def _on_item_selected(self, item, pspec):
        if item.props.selected:
            print('Item {} selected'.format(item.props.label))

    def populate(self, n_items=12):
        for i in range(1, n_items + 1):
            item = MenuItemModel()
            item.props.label = 'Option {0:d}'.format(i)

            self._model.append(item)

            item.connect('notify::selected', self._on_item_selected)

        self.select_item(0)

    def select_item(self, idx):
        if self._current_idx == idx:
            return self.get_child_at_index(self._current_idx)

        item = self.get_child_at_index(self._current_idx)
        if item is not None:
            item.props.selected = False

        self._current_idx = idx
        if self._current_idx < 0:
            self._current_idx = self.get_n_children()
        elif self._current_idx >= self.get_n_children():
            self._current_idx = 0

        item = self.get_child_at_index(self._current_idx)
        if item is not None:
            item.props.selected = True

        return item

    def select_prev(self):
        return self.select_item(self._current_idx - 1)

    def select_next(self):
        return self.select_item(self._current_idx + 1)

    def activate_item(self):
        item = self.get_child_at_index(self._current_idx)
        if item is not None:
            item.activate()

def on_key_press_event(stage, event):
    scroll = stage.get_first_child()
    menu = scroll.get_first_child()
    key = event.keyval

    if key == Clutter.KEY_q:
        Clutter.main_quit()
        return True

    if key == Clutter.KEY_Up:
        item = menu.select_prev()
        if item is not None:
            pos = Clutter.Point()
            (pos.x, pos.y) = item.get_position()
            scroll.scroll_to_point(pos)
            return True

    if key == Clutter.KEY_Down:
        item = menu.select_next()
        if item is not None:
            pos = Clutter.Point()
            (pos.x, pos.y) = item.get_position()
            scroll.scroll_to_point(pos)
            return True

    if key == Clutter.KEY_Return or key == Clutter.KEY_KP_Enter:
        menu.activate_item()
        return True

    return False

if __name__ == '__main__':
    Clutter.init(None)

    stage = Clutter.Stage(title='Actor Model', user_resizable=True)
    stage.connect('destroy', Clutter.main_quit)
    stage.connect('key-press-event', on_key_press_event)
    stage.show()

    scroll = Clutter.ScrollActor(name='scroll')
    scroll.set_position(0, 18)
    scroll.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.X_AXIS, factor=0.5))
    scroll.add_constraint(Clutter.BindConstraint(source=stage, coordinate=Clutter.BindCoordinate.HEIGHT, offset=-36))
    scroll.set_scroll_mode(Clutter.ScrollMode.VERTICALLY)
    scroll.set_easing_duration(250)
    stage.add_child(scroll)

    menu = Menu()
    scroll.add_child(menu)
    menu.populate()

    Clutter.main()
