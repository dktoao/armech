# seriallink.py
#
# Implementation of a robotic arm that is a series of links, hence the name
# serial link robot. Provides functions for forward kinematics, inverse
# kinematics, and dynamics calculations.

from numpy import identity, dot, zeros


class SerialLink:

    def __init__(self, links, base=None):
        """A serial link robot representation.
        :param links: a list of Link classes to create the robot structure
        :param base: the base of the robot which relates the serial link
        structure to it's place in the environment.
        :return: A SerialLink robot object
        """

        self.links = links
        self.base = base
        self.state = zeros(len(links))
        self.rotation = identity(3)
        self.translation = zeros((3, 1))

    def move_joints(self, q):
        """
        Updates the configuration of the robot
        Args:
            q: a vector of joint states in order from the base to the top
        """

        # Check input
        self.check_q(q)

        # Apply all transforms one by one
        global_transform = identity(4)
        for k, link in enumerate(self.links):
            global_state_transform = dot(
                global_transform, link.state_transform(q[k])
            )
            link.transform(
                rotation=global_state_transform[0:3, 0:3],
                translation=global_state_transform[0:3, 3]
            )
            global_transform = dot(global_state_transform, link.body_transform)

    def get_tool_trans(self, q):
        """Get the transform of the tool from the base of the robot given the
        state configuration "q"
        Args:
            q: state vector of the robot in meters and/or radians

        Returns: 4x4 transform matrix for the end of the arm
        """

        # Check inputs
        self.check_q(q)

        # Get the transform
        transform = identity(4)
        for k, link in enumerate(self.links):
            transform = dot(
                transform, link.state_transform(q[k])
            )
            transform = dot(
                transform, link.body_transform
            )

        return transform

    def check_q(self, q):
        """Check the state input vector and make sure that it is correct. Will
        error out if the input is not correct.

        Args:
            q: state vector of the robot in meters and/or radians

        Returns: None
        """

        # Make sure the correct input is given
        if len(q) != len(self.links):
            raise IndexError(
                    'The number of element in q is not equal to the number'
                    'of links'
            )
