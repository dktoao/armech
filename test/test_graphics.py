# test_graphics.py
#
# tests to show that the graphics are working properly

from numpy import float_
from numpy.testing import assert_array_almost_equal

from armech.graphics.workspace import Workspace
from armech.graphics.shapes import Box, Cylinder
from .testviewer import UserYesNoTestViewer
from armech.demo.robot import Simple3DOF

def test_box_normals_calculated_correctly():

    # Create a box object
    box = Box((-1.0, 1.0), (-1.0, 1.0), (-1.0, 1.0))
    # assert normals on each face are correct
    assert_array_almost_equal(
        box.face_normals,
        float_((
            (0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, -1.0, -1.0, 0.0, 0.0),
            (0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
            (-1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0),
        ))
    )


def test_workspace_and_other_objects_display_correctly():

    # Create and fill a workspace with objects
    ws = Workspace((-4.0, 4.0), (-6.0, 6.0), (0.0, 10.0), face_color=(0.8, 0.8, 0.8))
    # Cube Obstacles
    cube_obstacle = Box((-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), face_color=(1.0, 1.0, 0.0))
    ws.add_obstacle('cube_obstacle', cube_obstacle)
    cube_obstacle_x = Box((-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), face_color=(1.0, 0.0, 0.0))
    cube_obstacle_x.set_transform(translation=(2.0, 0.0, 0.0))
    ws.add_obstacle('cube_obstacle_x', cube_obstacle_x)
    cube_obstacle_y = Box((-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), face_color=(0.0, 1.0, 0.0))
    cube_obstacle_y.set_transform(translation=(0.0, 2.0, 0.0))
    ws.add_obstacle('cube_obstacle_y', cube_obstacle_y)
    cube_obstacle_z = Box((-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5), face_color=(0.0, 0.0, 1.0))
    cube_obstacle_z.set_transform(translation=(0.0, 0.0, 2.0))
    ws.add_obstacle('cube_obstacle_z', cube_obstacle_z)
    # Cylinder Obstacle
    cylinder_obstacle = Cylinder(2, 0.5)
    cylinder_obstacle.set_transform(translation=(3.0, 3.0, 0.0))
    ws.add_obstacle('cylinder_obstacle', cylinder_obstacle)

    # Create a viewer and display the scene
    view = UserYesNoTestViewer(ws, "Is the workspace displayed correctly?")
    view.show()

test_simple3dof_displays_correctly():

    # Create a workspace
    ws = Workspace((-2.0, 2.0), (-2.0, 2.0), (0.0, 4.0), face_color=(0.8, 0.8, 0.8))
    # Create robot and put it in the workspace
    robot = Simple3DOF()
