# seriallink.py
#
# Implementation of a robotic arm that is a series of links, hence the name
# serial link robot. Provides functions for forward kinematics, inverse
# kinematics, and dynamics calculations.

from numpy import identity, dot, zeros, concatenate


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
        self.global_transform = identity(4)

    def set_global_transform(self, rotation=None, translation=None):
        """Set the global transform for the overall arm assembly

        Args:
            rotation: [3x3] symmetric float array describing the rotation of
                      the robot.
            translation: [3x1] float array describing the x,y,z position of
                         the robot.

        """

        # Set input parameters to the correct type
        if rotation is not None:
            rotation = float_(rotation).reshape(3, 3)
        else:
            rotation = self.global_transform[0:3, 0:3]
        if translation is not None:
            translation = float_(translation).reshape(3, 1)
        else:
            translation = self.global_transform[0:3, 3]

        self.global_transform = concatenate(
            concatenate((rotation, translation), axis=1),
            float_([0.0, 0.0, 0.0, 1.0]).reshape(1, 4)
        )

    def move_joints(self, q):
        """
        Updates the configuration of the robot
        Args:
            q: a vector of joint states in order from the base to the top
        """

        # Check input
        self.check_q(q)

        # Apply all transforms one by one
        global_transform = self.global_transform
        for k, link in enumerate(self.links):
            global_state_transform = dot(
                global_transform, link.state_transform(q[k])
            )
            link.transform(
                rotation=global_state_transform[0:3, 0:3],
                translation=global_state_transform[0:3, 3]
            )
            global_transform = dot(global_state_transform, link.body_transform)

    def get_tool_trans(self, q, local=True):
        """Get the transform of the tool from the base of the robot given the
        state configuration "q"
        Args:
            q: state vector of the robot in meters and/or radians
            local: bool, get transform local to the robot, if False will give
                   the transform from the robots global_coordinates

        Returns: 4x4 transform matrix for the end of the arm
        """

        # Check inputs
        self.check_q(q)

        # Set base transform
        if local:
            transform = identity(4)
        else:
            transform = self.global_transform

        # Loop through links and calculate transform
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
