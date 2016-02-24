# link.py
#
# Implementation of the Link class that represents a link in a chain of
# serial links.
#
# MAJOR TODO: rewrite this whole class using the GraphicalBody or PhysicalBody class
#

from numpy import array, float_, cos, sin

from armech.core.rigidbody import RigidBody


class Link(RigidBody):

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

        super(Link, self).__init__()

        # Initialize values
        self.a = float_(a)
        self.alpha = float_(alpha)
        self.d = float_(d)
        self.theta = float_(theta)
        if self.joint_type == 'revolute':
            self.tform = self.get_revolute_tform()
        elif self.joint_type == 'prismatic':
            self.tform = self.prismatic_tform
        else:
            raise ValueError('type must be either "revolute" or "prismatic"')

    def get_revolute_tform(self):
        """
        Return the transform from the end of the previous joint to the end of
        this joint as a function of the joint angle theta

        Returns: a function tform(theta)
        """
        # Get values
        a = self.a
        alpha = self.alpha
        d = self.d

        def tform(theta):
            array([
                [cos(theta), sin(theta), 0.0, a],
                [-sin(theta)*cos(alpha), cos(alpha)]
            ])