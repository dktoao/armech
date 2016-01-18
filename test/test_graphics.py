# test_graphics.py
#
# tests to show that the graphics are working properly

from armech.graphics.workspace import Workspace
from armech.graphics.shapes import Box, Cylinder
from armech.graphics.workspaceviewer import BaseViewer


def test_workspace_and_other_objects_display_correctly():

    # Create and fill a workspace with objects
    ws = Workspace((-4.0, 4.0), (-6.0, 6.0), (0.0, 10.0))
    # Cube Obstacle
    cube_obstacle = Box((-0.5, 0.5), (-0.5, 0.5), (-0.5, 0.5))
    cube_obstacle.set_transform(translation=(1.0, 1.0, 9.0))
    ws.add_obstacle('cube_obstacle', cube_obstacle)
    # Cylinder Obstacle
    cylinder_obstacle = Cylinder(4, 0.5)
    cylinder_obstacle.set_transform(translation=(2.0, 2.0, 2.0))
    ws.add_obstacle('cylinder_obstacle', cylinder_obstacle)

    # Create a viewer and display the scene
    view = BaseViewer(ws)
    view.show()