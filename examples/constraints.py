from gi.repository import Clutter

if __name__ == '__main__':
    Clutter.init(None)

    # The main stage
    stage = Clutter.Stage(title='Constraints', user_resizable=True)
    stage.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.ALUMINIUM_1)
    stage.connect('destroy', Clutter.main_quit)

    # First actor, with a fixed (100, 25) size
    layer_a = Clutter.Actor()
    layer_a.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.SCARLET_RED)
    layer_a.set_size(100, 25)
    stage.add_child(layer_a)

    # The first actor is anchored to the center of the stage
    layer_a.add_constraint(Clutter.AlignConstraint(source=stage, align_axis=Clutter.AlignAxis.BOTH, factor=0.5))

    # Second actor, with no explicit size
    layer_b = Clutter.Actor()
    layer_b.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.BUTTER_DARK)
    stage.add_child(layer_b)

    # The second actor tracks the X coordinate and the width of the first actor
    layer_b.add_constraint(Clutter.BindConstraint(source=layer_a, coordinate=Clutter.BindCoordinate.X))
    layer_b.add_constraint(Clutter.BindConstraint(source=layer_a, coordinate=Clutter.BindCoordinate.WIDTH))

    # The second actor is snapped between the bottom edge of the first actor
    # and the bottom edge of the stage; vertical spacing of 10px is added for
    # padding
    layer_b.add_constraint(Clutter.SnapConstraint(source=layer_a,
                                                  from_edge=Clutter.SnapEdge.TOP,
                                                  to_edge=Clutter.SnapEdge.BOTTOM,
                                                  offset=10))
    layer_b.add_constraint(Clutter.SnapConstraint(source=stage,
                                                  from_edge=Clutter.SnapEdge.BOTTOM,
                                                  to_edge=Clutter.SnapEdge.BOTTOM,
                                                  offset=-10))

    # The third actor, again with no explicit size
    layer_c = Clutter.Actor()
    layer_c.props.background_color = Clutter.Color.get_static(Clutter.StaticColor.CHAMELEON_LIGHT)
    stage.add_child(layer_c)

    # Like the second actor, the third one also track the X coordinate and
    # width of the first actor
    layer_c.add_constraint(Clutter.BindConstraint(source=layer_a, coordinate=Clutter.BindCoordinate.X))
    layer_c.add_constraint(Clutter.BindConstraint(source=layer_a, coordinate=Clutter.BindCoordinate.WIDTH))

    # The third layer is snapped between the top of the first layer and
    # the top of the stage
    layer_c.add_constraint(Clutter.SnapConstraint(source=layer_a,
                                                  from_edge=Clutter.SnapEdge.BOTTOM,
                                                  to_edge=Clutter.SnapEdge.TOP,
                                                  offset=-10))
    layer_c.add_constraint(Clutter.SnapConstraint(source=stage,
                                                  from_edge=Clutter.SnapEdge.TOP,
                                                  to_edge=Clutter.SnapEdge.TOP,
                                                  offset=10))

    stage.show()

    Clutter.main()
