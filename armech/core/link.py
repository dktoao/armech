# link.py
#
# Implementation of the Link class that represents a link in a chain of
# serial links.
#
# MAJOR TODO: rewrite this whole class using the GraphicalBody or PhysicalBody class
#

from numpy import float_, cos, sin

from armech.config import JOINT_REVOLUTE, JOINT_PRISMATIC
from armech.core.rigidbody import RigidBody


# JointType class for consistency

class LinkDH(RigidBody):

    def __init__(self, a=0.0, alpha=0.0, d=0.0, theta=0.0, joint_type):
        """
        A link in a serial chain robot described by Denavit-Hartenberg (DH)
        parameters.
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
        self.tform = self.get_tform()
        if joint_type == JOINT_REVOLUTE:
            self.joint_type = JOINT_REVOLUTE
            self.joint_type_str = 'Revolute Joint'
        elif joint_type == JOINT_PRISMATIC:
            self.joint_type = JOINT_REVOLUTE
            self.joint_type_str = 'Prismatic Joint'
        else:
            raise ValueError(
                'type must be either constants.JOINT_REVOLUTE or '
                'constants.JOINT_PRISMATIC'
            )

    def get_tform(self):
        """
        Return the transform from the end of the previous joint to the end of
        this joint as a function of the joint angle theta

        Returns: a function tform(q) where q is the state of the joint
                 (Angular or Linear displacement)
        """
        if self.joint_type == JOINT_REVOLUTE:
            return lambda q: float_([
                [cos(self.theta + q), sin(self.theta + q)*cos(self.alpha),
                 sin(self.alpha)*sin(self.theta + q), self.a*cos(self.theta + q)],
                [-sin(self.theta + q), cos(self.alpha)*cost(self.theta + q),
                 sin(self.alpha)*cos(self.theta + q), -self.a*sin(self.theta + q)],
                [0, -sin(self.alpha), cos(self.alpha), self.d],
                [0, 0, 0, 1],
            ])
        elif self.joint_type == JOINT_PRISMATIC:
            return lambda q: float_([
                [cos(self.theta), sin(self.theta)*cos(self.alpha + q),
                 sin(self.alpha + q)*sin(self.theta), self.a*cos(self.theta)],
                [-sin(self.theta), cos(self.alpha + q)*cost(self.theta),
                 sin(self.alpha + q)*cos(self.theta), -self.a*sin(self.theta)],
                [0, -sin(self.alpha + q), cos(self.alpha + q), self.d],
                [0, 0, 0, 1],
            ])
        else:
            raise ValueError(
                'type must be either constants.JOINT_REVOLUTE or '
                'constants.JOINT_PRISMATIC'
            )
