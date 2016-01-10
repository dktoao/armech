# body.py
#
# Contains the GraphicalBody class that allows rendering via PyOpenGL and
# various functions along with a way to update the transformation matrix

# TODO: load_body needs to be an inheritable member function

from numpy import dot, identity, float_, int_, zeros, min, max


class GraphicalBody:

    def __init__(self, vertices, edges, faces, color=(1.0, 1.0, 1.0)):
        """
        Create a graphical body.
        :param vertices: 3xN array of [x, y, z]^T vertices
        :param edges: 2xK array of edge vertex indices
        :param faces: 3xK array of face vertex indices
        :return obj: GraphicalBody object
        """

        # initialize values
        self.vertices = float_(vertices)
        self.edges = float_(edges)
        self.faces = float_(faces)
        self.color = float_(color)
        self.n_vertices = vertices.shape[0]
        self.n_edges = edges.shape[0]
        self.n_faces = faces.shape[0]

        # find the bounding box
        self.bounds_x = float_((min(self.vertices[0, :]), max(self.vertices[0, :])))
        self.bounds_y = float_((min(self.vertices[1, :]), max(self.vertices[1, :])))
        self.bounds_z = float_((min(self.vertices[2, :]), max(self.vertices[2, :])))

        # Set the transform to the world
        self.rotation = identity(3)
        self.translation = zeros(3, 1)
        self.world_vertices = vertices

    def set_transform(self, rotation, translation):
        """
        Set the transform from the object to the world
        :param rotation: 3x3 rotation matrix from the body to world
        :param translation: 3x1 vector to the body coordinate system
        """

        # Set values
        self.rotation = float_(rotation)
        self.translation = float_(translation)

        # Apply the transform
        self.world_vertices = dot(self.rotation, self.vertices) + self.translation


def load_obj(obj_file_name, color=(1.0, 1.0, 1.0)):
    """
    Helper method to create a Graphical object from a .obj file
    :param obj_file_name: link to an .obj file containing the vertex and face info
    :return obj: a GraphicalBody object
    """

    # Read in the file and extract vertices and faces
    obj_file = open(obj_file_name, 'r')
    if not obj_file:
        raise IOError('Could not open "{}"'.format(obj_file_name))

    # Parse the file and store vertices and faces
    vertices = []
    faces = []
    for line in obj_file:
        data = line.strip().split('\s')
        if data[0] == 'v':
            vertices.append(tuple(data[1:]))
        elif data[0] == 'f':
            faces.append(tuple(data[1:]))

    vertices = float_(vertices).transpose()
    faces = int_(faces).transpose()

    return GraphicalBody(vertices, [], faces, color)