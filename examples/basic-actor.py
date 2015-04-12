import sys

from gi.repository import Clutter

class ToggleActor(Clutter.Actor):
    def __init__(self):
        Clutter.Actor.__init__(self)
        self._toggled = False

    @property
    def toggled(self):
        return self._toggled

    def toggle(self):
        if self._toggled:
            self._toggled = False
        else:
            self._toggled = True

def animate_color(actor, event):
    actor.toggle()

    end_color = None
    if actor.toggled:
        end_color = Clutter.Color.get_static(Clutter.StaticColor.BLUE)
    else:
        end_color = Clutter.Color.get_static(Clutter.StaticColor.RED)

    with actor.easing_state(500, Clutter.AnimationMode.LINEAR):
        actor.props.background_color = end_color

    return True

def on_transition_stopped(actor, transition_name, is_finished):
    if transition_name == 'rotation-angle-y':
        with actor.easing_state():
            actor.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, 0)

def animate_rotation(actor, event):
    with actor.easing_state(1000):
        actor.set_rotation_angle(Clutter.RotateAxis.Y_AXIS, 360.0)

    return True

def on_crossing(actor, event):
    z_pos = 0
    if event.type == Clutter.EventType.ENTER:
        z_pos = -250

    with actor.easing_state(500, Clutter.AnimationMode.EASE_OUT_BOUNCE):
        actor.set_z_position(z_pos)

    return True

if __name__ == '__main__':
    stage = Clutter.Stage(title="Three Flowers in a Vase")
    stage.props.user_resizable = True
    stage.connect('destroy', Clutter.main_quit)

    vase = Clutter.Actor(name='vase')
    vase.props.layout_manager = Clutter.BoxLayout()
    vase.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.SKY_BLUE_LIGHT)
    vase.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))
    stage.add_child(vase)

    flowers = []

    flower = ToggleActor()
    flower.set_name('flower.1')
    flower.set_size(128, 128)
    flower.set_margin_left(12)
    flower.set_background_color(Clutter.Color.get_static(Clutter.StaticColor.RED))
    flower.props.reactive = True
    flower.connect('button-press-event', animate_color)
    vase.add_child(flower)
    flowers.append(flower)

    flower = Clutter.Actor(name='flower.2')
    flower.set_size(128, 128)
    flower.set_margin_top(12)
    flower.set_margin_bottom(12)
    flower.set_margin_left(6)
    flower.set_margin_right(6)
    flower.set_background_color(Clutter.Color.get_static(Clutter.StaticColor.YELLOW))
    flower.set_reactive(True)
    flower.connect('enter-event', on_crossing)
    flower.connect('leave-event', on_crossing)
    vase.add_child(flower)
    flowers.append(flower)

    # The third one is green
    flower = Clutter.Actor(name='flower.3')
    flower.set_size(128, 128)
    flower.set_margin_right(12)
    flower.set_background_color(Clutter.Color.get_static(Clutter.StaticColor.GREEN))
    flower.set_pivot_point(0.5, 0.0)
    flower.props.reactive = True
    flower.connect('button-press-event', animate_rotation)
    flower.connect('transition-stopped', on_transition_stopped)
    vase.add_child(flower)
    flowers.append(flower)

    stage.show()

    Clutter.main()
