# workspace.py
#
# Workspace object that is a rectangular room which can be populated with
# robots, graspable objects and obstacles.

from armech.graphics.graphicalbody import GraphicalBody
from armech.graphics.shapes import Box


class Workspace(Box):

    def __init__(self, bounds_x, bounds_y, bounds_z,
                 face_color=(0.0, 1.0, 0.0),
                 edge_color=(0.2, 0.2, 0.2)):
        """
        Create a workspace object
        :param bounds_x: 1x2 array of the lower and upper bounds of the
        workspace's "x" dimension
        :param bounds_y: 1x2 array of the lower and upper bounds of the
        workspace's "y" dimension
        :param bounds_z: 1x2 array of the lower and upper bounds of the
        workspace's "z" dimension
        :param face_color: 1x3 array for the face color
        :param edge_color: 1x3 array for the face color
        :return: A Workspace object
        """

        # Initialize Box
        super(Workspace, self).__init__(bounds_x, bounds_y, bounds_z, face_color, edge_color, False)

        # Create a list of obstacles
        self.obstacles = {}

    def add_obstacle(self, name, obstacle):
        """
        Adds an obstacle to the scene, can be accessed by name
        :param name: string; name given to the object
        :param obstacle: GraphicalBody object to add to the scene
        """

        # Check that the obstacle is a GraphicalBody
        if not isinstance(obstacle, GraphicalBody):
            raise ValueError(
                'The obstacle must be an instance of GraphicalBody'
            )

        # Add the obstacle to the obstacles dictionary
        self.obstacles[name] = obstacle
