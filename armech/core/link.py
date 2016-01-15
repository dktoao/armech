# link.py
#
# Implementation of the Link class that represents a link in a chain of
# serial links.
#
# MAJOR TODO: rewrite this whole class using the GraphicalBody or PhysicalBody class
#

from numpy import array, float


class Link:

    def __init__(self, a, alpha, d, theta, joint_type):
        """
        A link in a serial chain robot
        :param a: the distance from z(i) to z(i+1) measured along x(i) (meters)
        :param alpha: the angle from z(i) to z(i+1) measured about x(i) (radians)
        :param d: the distance from x(i-1) to x(i) measured along z(i) (meters)
        :param theta: the angle from x(i-1) to x(i) measured about z(i) (radians)
        :param joint_type: type of joint connecting the link, either
        'revolute' or 'prismatic'
        :return: A Link object
        """

        # Initialize values
        self.a = float(a)
        self.alpha = float(alpha)
        self.d = float(d)
        self.theta = float(theta)
        if self.joint_type == 'revolute':
            self.d = float(d)
            self.theta = None
            self.joint_type = joint_type
        elif self.joint_type == 'prismatic':
            self.theta = float(theta)
            self.d = None
            self.joint_type = joint_type
        else:
            raise ValueError('type must be either "revolute" or "prismatic"')
        self.obj_file = None
        self.color = None
        self.mass = None
        self.center_of_mass = None
        self.inertia_matrix = None

        # Turn of other functionality
        self.is_graphic = False
        self.is_dynamic = False

    def set_graphic(self, obj_file, color=(1.0, 1.0, 0.0)):
        """
        Set the geometry and color of the link for simulation
        :param obj_file: the .obj file containing the part's geometry
        :param color: the color of the part as an rgb tuple e.g. (1.0, 1.0, 0.0)
        """

        # Set values
        self.obj_file = obj_file
        self.color = color

        # TODO: Read in the file and get ready for display

        # Enable graphics
        self.is_graphic = True

    def set_dynamics(self, mass, center_of_mass,
                     moment_of_inertia, product_of_inertia):
        """
        Sets the dynamic parameters of the link
        :param mass: Mass of the link (kg)
        :param center_of_mass: distance from the part origin to the center
        of mass (x, y, z) (meters)
        :param moment_of_inertia: Moment of inertia of the link about the
        origin (Ixx, Iyy, Izz) (kg m^2)
        :param product_of_inertia: Product of inertia of the link about the
        origin (Iyz, Ixz, Ixy) (kg m^2)
        :return:
        """

        # Set values
        self.mass = mass
        self.center_of_mass = center_of_mass
        self.inertia_matrix = array([
            [moment_of_inertia[0], product_of_inertia[0], product_of_inertia[1]],
            [product_of_inertia[0], moment_of_inertia[1], product_of_inertia[2]],
            [product_of_inertia[1], product_of_inertia[2], moment_of_inertia[2]],
        ])

        # Enable dynamics
        self.is_dynamic = True
