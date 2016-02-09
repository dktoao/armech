# body.py
#
# Contains the GraphicalBody class that allows rendering via PyOpenGL and
# various functions along with a way to update the transformation matrix

from numpy import dot, identity, float_, int_, zeros, min, max, cross
from numpy.linalg import norm
from OpenGL.GL import glVertex3fv, glColor3fv, glNormal3fv, glMaterialfv, \
    GL_DIFFUSE, GL_AMBIENT, GL_FRONT

# Constants
DEFAULT_FACE_COLOR = float_((0.0, 1.0, 1.0))
DEFAULT_EDGE_COLOR = float_((0.2, 0.2, 0.2))


class GraphicalBody:

    def __init__(self):
        """
        Create a graphical body that can be transformed and rendered.
        :return obj: GraphicalBody object
        """

        # initialize values
        self.has_graphics = False
        self.vertices = float_([])
        self.edges = float_([])
        self.faces = float_([])
        self.face_normals = float_([])
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
        self.world_vertices = float_([])
        self.world_face_normals = float_([])

    def set_transform(self, **kwargs):
        """
        Set the transform from the object to the world coordinate system
        :param rotation: 3x3 rotation matrix from the body to world
        :param translation: 3x1 vector to the body coordinate system
        """
        rotation = kwargs.get('rotation')
        translation = kwargs.get('translation')

        # Set values
        if rotation:
            self.rotation = float_(rotation)
        if translation:
            self.translation = float_(translation).reshape((3, 1))

        # Apply the transform
        if self.has_graphics:
            self.world_vertices = dot(self.rotation, self.vertices) + \
                self.translation
            self.world_face_normals = dot(self.rotation, self.face_normals)

    def set_graphics(self, vertices, edges, faces,
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
        self.n_vertices = self.vertices.shape[1]
        self.n_edges = self.edges.shape[0]
        self.n_faces = self.faces.shape[0]

        # find the face normals
        self.face_normals = zeros((3, self.n_faces))
        for k, idx_vertices in enumerate(faces):
            vec1 = self.vertices[:, idx_vertices[1]] - self.vertices[:, idx_vertices[0]]
            vec2 = self.vertices[:, idx_vertices[2]] - self.vertices[:, idx_vertices[0]]
            normal = cross(vec1, vec2)
            self.face_normals[:, k] = normal/norm(normal)

        # find the bounding box
        self.bounds_x = float_((min(self.vertices[0, :]),
                                max(self.vertices[0, :])))
        self.bounds_y = float_((min(self.vertices[1, :]),
                                max(self.vertices[1, :])))
        self.bounds_z = float_((min(self.vertices[2, :]),
                                max(self.vertices[2, :])))

        # set the has_obj flag
        self.has_graphics = True

        # Update world vertices and normals
        self.set_transform()

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
        self.set_graphics(vertices, [], faces, face_color, edge_color)

    def render_faces(self):
        """
        Draws the object faces on the OpenGL canvas.
        """
        if self.has_graphics:
            glColor3fv(self.face_color)
            #glMaterialfv(GL_FRONT, GL_DIFFUSE, self.face_color)
            #glMaterialfv(GL_FRONT, GL_AMBIENT, self.face_color)
            for k, face in enumerate(self.faces):
                glNormal3fv(self.world_face_normals[:, k])
                for idx_vertex in face:
                    glVertex3fv(self.world_vertices[:, idx_vertex])

    def render_edges(self):
        """
        Draws the object edges on the OpenGL canvas.
        """
        if self.has_graphics:
            glColor3fv(self.edge_color)
            for edge in self.edges:
                for idx_vertex in edge:
                    glVertex3fv(self.world_vertices[:, idx_vertex])
