# shapes.py
#
# Functions for getting vertexes, edges and faces for simple shapes such as
# rectangular boxes, cylinders and spheres.

from numpy import pi, sin, cos
from .graphicalbody import GraphicalBody


class Box(GraphicalBody):

    def __init__(self, bounds_x, bounds_y, bounds_z,
                 face_color=(0.0, 0.0, 1.0), outward_normals=True):
        """
        Create a graphical body which is a 3d rectangle
        :param bounds_x: 1x2 array of the lower and upper bounds of the
        box's "x" dimension
        :param bounds_y: 1x2 array of the lower and upper bounds of the
        box's "y" dimension
        :param bounds_z: 1x2 array of the lower and upper bounds of the
        box's "z" dimension
        :param face_color: RGB color as a 3 element float array with
        values 0.0 - 1.0
        :param outward_normals: bool, if True will cause the box to be
        displayed inside out
        """

        super(Box, self).__init__()

        # Create the geometry
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

        if outward_normals:
            faces = (
                (0, 3, 1),
                (1, 3, 2),
                (0, 5, 4),
                (1, 5, 0),
                (1, 2, 5),
                (2, 6, 5),
                (2, 3, 6),
                (3, 7, 6),
                (3, 4, 7),
                (0, 4, 3),
                (4, 5, 7),
                (5, 6, 7),
            )
        else:
            faces = (
                (0, 1, 3),
                (1, 2, 3),
                (0, 4, 5),
                (1, 0, 5),
                (1, 5, 2),
                (2, 5, 6),
                (2, 6, 3),
                (3, 6, 7),
                (3, 7, 4),
                (0, 3, 4),
                (4, 7, 5),
                (5, 7, 6),
            )

        self.set_graphics(vertices, faces, face_color)


class Cylinder(GraphicalBody):

    def __init__(self, height, radius, n_points=1,
                 face_color=(0.0, 0.0, 1.0)):
        """
        Get the vertices, edges and faces of a cylinder
        :param height: height of cylinder from -z to z
        :param radius: radius of the cylinder
        :param n_points: points to draw on the top and bottom curves
        :param face_color: RGB color as a 3 element float array with
        values 0.0 - 1.0
        """

        super(Cylinder, self).__init__()

        # Calculate the number of points in each circle
        n_circ_pnts = 4 + 4*n_points
        angle_vertices = (pi/2)/(n_points + 1)

        # Generate vertices
        vertices = [
            (0.0, 0.0, -height/2),  # bottom center
            (0.0, 0.0, height/2),   # top center
        ]
        for z in [-height/2, height/2]:
            for n in range(n_circ_pnts):
                x = radius*cos(n*angle_vertices)
                y = radius*sin(n*angle_vertices)
                vertices.append((x, y, z))

        # Generate faces
        faces = []
        for n in range(n_circ_pnts):
            idx_cur = n+2
            if n+2 > n_circ_pnts:
                idx_next = 2
            else:
                idx_next = n+3
            faces.append((0, idx_next, idx_cur))  # bottom face
            faces.append((1, idx_cur+n_circ_pnts, idx_next+n_circ_pnts))  # top face
            faces.append((idx_cur, idx_next, idx_cur+n_circ_pnts))  # side face 1
            faces.append((idx_next, idx_next+n_circ_pnts, idx_cur+n_circ_pnts))

        # Initialize geometry
        self.set_graphics(vertices, faces, face_color)


# TODO: class Sphere(GraphicalBody):
# TODO: class Cone(GraphicalBody):
