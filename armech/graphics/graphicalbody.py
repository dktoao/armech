# body.py
#
# Contains the GraphicalBody class that allows rendering via PyOpenGL and
# various functions along with a way to update the transformation matrix

from numpy import dot, identity, float_, int_, zeros, min, max
from OpenGL.GL import glVertex3fv, glColor3fv

DEFAULT_FACE_COLOR = float_((0.0, 1.0, 1.0))
DEFAULT_EDGE_COLOR = float_((0.2, 0.2, 0.2))


class GraphicalBody:

    def __init__(self):
        """
        Create a graphical body that can be transformed and rendered.
        :return obj: GraphicalBody object
        """

        # initialize values
        self.has_obj = False
        self.vertices = float_([])
        self.edges = float_([])
        self.faces = float_([])
        self.face_color = float_(DEFAULT_FACE_COLOR)
        self.edge_color = float_(DEFAULT_EDGE_COLOR)
        self.n_vertices = float_(0)
        self.n_edges = float_(0)
        self.n_faces = float_(0)
        self.bounds_x = float_((0, 0))
        self.bounds_y = float_((0, 0))
        self.bounds_z = float_((0, 0))
        self.rotation = identity(3)
        self.translation = zeros((3, 1))
        self.world_vertices = None

    def set_transform(self, rotation, translation):
        """
        Set the transform from the object to the world coordinate system
        :param rotation: 3x3 rotation matrix from the body to world
        :param translation: 3x1 vector to the body coordinate system
        """

        # Set values
        self.rotation = float_(rotation)
        self.translation = float_(translation)

        # Apply the transform
        self.world_vertices = dot(self.rotation, self.vertices) + \
            self.translation

    def set_geometry(self, vertices, edges, faces,
                     face_color=DEFAULT_FACE_COLOR,
                     edge_color=DEFAULT_EDGE_COLOR):
        """
        Sets the geometry of the part for graphical display
        :param vertices: list of 3 value vertices (x, y, z)
        :param edges: list of two vertices to connect by edge
        :param faces: list of three vertices to connect with triangle
        :param face_color: 1x3 color of the object faces, in RGB format
        e.g. [0.0, 1.0, 0.5]
        :param edge_color: 1x3 color of the object edges, in RGB format
        """

        # Set the appropriate values
        self.vertices = float_(vertices).transpose()
        self.edges = int_(edges)
        self.faces = int_(faces)
        self.face_color = float_(face_color)
        self.edge_color = float_(edge_color)
        self.n_vertices = self.vertices.shape[0]
        self.n_edges = self.edges.shape[0]
        self.n_faces = self.faces.shape[0]

        # find the bounding box
        self.bounds_x = float_((min(self.vertices[0, :]),
                                max(self.vertices[0, :])))
        self.bounds_y = float_((min(self.vertices[1, :]),
                                max(self.vertices[1, :])))
        self.bounds_z = float_((min(self.vertices[2, :]),
                                max(self.vertices[2, :])))

        # find the word vertices
        self.world_vertices = dot(self.rotation, self.vertices) + \
            self.translation

        # set the has_obj flag
        self.has_obj = True

    def load_obj(self, obj_file_name, face_color=DEFAULT_FACE_COLOR,
                 edge_color=DEFAULT_EDGE_COLOR):
        """
        Load the visual representation of the body from an .obj file.
        :param obj_file_name: link to the .obj file containing vertex and face
        info
        :param face_color: color of the object faces, in RGB format
        e.g. (0.0, 1.0, 0.5)
        :param edge_color: color of the object edges, in RGB format
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

        # Set the values
        self.set_geometry(vertices, [], faces, face_color, edge_color)

    def render_faces(self):
        """
        Draws the object faces on the OpenGL canvas.
        """
        if self.has_obj:
            glColor3fv(self.face_color)
            for face in self.faces:
                for idx_vertex in face:
                    glVertex3fv(self.vertices[:, idx_vertex])
        else:
            pass

    def render_edges(self):
        """
        Draws the object edges on the OpenGL canvas.
        """
        if self.has_obj:
            glColor3fv(self.edge_color)
            for edge in self.edges:
                for idx_vertex in edge:
                    glVertex3fv(self.vertices[:, idx_vertex])
        else:
            pass