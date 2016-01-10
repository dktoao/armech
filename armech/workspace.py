# workspace.py
#
# Workspace object that is a rectangular room which can be populated with
# robots, graspable objects and obstacles.

from armech.graphics.graphicalbody import GraphicalBody


class Workspace(GraphicalBody):

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

        # Initialize GraphicalBody
        super(Workspace, self).__init__()

        # Establish room geometry
        vertices = (
            (bounds_x[0], bounds_y[0], bounds_z[0]),
            (bounds_x[1], bounds_y[0], bounds_z[0]),
            (bounds_x[1], bounds_y[1], bounds_z[0]),
            (bounds_x[0], bounds_y[1], bounds_z[0]),
            (bounds_x[0], bounds_y[0], bounds_z[1]),
            (bounds_x[1], bounds_y[0], bounds_z[1]),
            (bounds_x[1], bounds_y[1], bounds_z[1]),
            (bounds_x[0], bounds_y[1], bounds_z[1]),
        )
        edges = (
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        )
        faces = (
            (0, 1, 3),
            (1, 2, 3),
            (0, 4, 5),
            (1, 0, 5),
            (1, 5, 2),
            (2, 1, 6),
            (2, 6, 3),
            (3, 6, 7),
            (3, 7, 4),
            (0, 3, 4),
            (4, 7, 5),
            (5, 7, 6),
        )

        self.set_geometry(vertices, edges, faces, face_color, edge_color)