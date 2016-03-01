# linkdh.py
#
# Implementation of the the LinkDH class that creates a representation of a
# link in a serial link robot described by Denavit-Hartenberg (DH) parameters
#

from numpy import float_, cos, sin

from armech.config import JOINT_REVOLUTE, JOINT_PRISMATIC
from armech.core.rigidbody import RigidBody


# JointType class for consistency

class LinkDH(RigidBody):

    def __init__(self, joint_type, a=0.0, alpha=0.0, d=0.0, theta=0.0):
        """
        A link in a serial chain robot described by Denavit-Hartenberg (DH)
        parameters.
        :param a: the distance from z(i) to z(i+1) measured along x(i) (meters)
        :param alpha: the angle from z(i) to z(i+1) measured about x(i) (radians)
        :param d: the distance from x(i-1) to x(i) measured along z(i) (meters)
        :param theta: the angle from x(i-1) to x(i) measured about z(i) (radians)
        :param joint_type: type of joint connecting the link, either
        armech.constants.REVOLUTE_JOINT or PRISMATIC_JOINT
        :return: A Link object
        """

        # Initialize Graphical Body
        super(LinkDH, self).__init__()

        # Initialize values
        self.a = float_(a)
        self.alpha = float_(alpha)
        self.d = float_(d)
        self.theta = float_(theta)
        self.body_transform = float_([
            [1.0,              0.0,             0.0, self.a],
            [0.0,  cos(self.alpha), sin(self.alpha),    0.0],
            [0.0, -sin(self.alpha), cos(self.alpha),    0.0],
            [0.0,              0.0,             0.0,    1.0],
        ])
        self.state_transform = self.get_state_transform()
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

    def get_state_transform(self):
        """
        Get the state transform (depending on d or theta) depending on the
        joint_type of the link.

        Returns:
            A function f(q) that calculates the transform from the base of
            the arm to the arm based on it's general coordinate q (theta or d)
        """

        if self.joint_type == JOINT_REVOLUTE:
            return lambda q: float_([
                [cos(self.theta + q),  sin(self.theta + q), 0.0, 0.0],
                [-sin(self.theta + 1), cos(self.theta + q), 0.0, 0.0],
                [0.0,                  0.0,                 1.0, self.d],
                [0.0,                  0.0,                 0.0, 1.0],
            ])
        elif self.joint_type == JOINT_PRISMATIC:
            return lambda q: float_([
                [cos(self.theta),  sin(self.theta), 0.0, 0.0],
                [-sin(self.theta), cos(self.theta), 0.0, 0.0],
                [0.0,              0.0,             1.0, self.d + q],
                [0.0,              0.0,             0.0, 1.0],
            ])
        else:
            raise ValueError(
                'type must be either constants.JOINT_REVOLUTE or '
                'constants.JOINT_PRISMATIC'
            )