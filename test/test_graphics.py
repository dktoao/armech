# test_graphics.py
#
# tests to show that the graphics are working properly

from armech.graphics.workspace import Workspace
from armech.graphics.shapes import Box, Cylinder
from armech.graphics.workspaceviewer import BaseViewer


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
    #cylinder_obstacle = Cylinder(4, 0.5)
    #cylinder_obstacle.set_transform(translation=(2.0, 2.0, 2.0))
    #ws.add_obstacle('cylinder_obstacle', cylinder_obstacle)

    # Create a viewer and display the scene
    view = BaseViewer(ws)
    view.show()
