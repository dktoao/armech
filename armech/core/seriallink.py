# seriallink.py
#
# Implementation of a robotic arm that is a series of links, hence the name
# serial link robot. Provides functions for forward kinematics, inverse
# kinematics, and dynamics calculations.

from numpy import identity, dot, zeros, concatenate, float_


class SerialLink:

    # TODO: global_transform -> global_translation, global_rotation
    def __init__(self, links, base=None,
                 global_rotation=None,
                 global_translation=None):
        """A serial link robot representation.
        :param links: a list of Link classes to create the robot structure
        :param base: the base of the robot which relates the serial link
        :param global_rotation: [3x3] float orthonormal matrix describing the
        rotation of the robot.
        :param global_translation: [3x1] float matrix describing the x,y,z
        position of the robot.
        structure to it's place in the environment.
        :return: A SerialLink robot object
        """

        # Class members
        self.links = links
        self.num_links = len(links)
        self.base = base
        self.state = zeros(self.num_links, dtype='float')
        self.link_transforms = zeros((4, 4, self.num_links), dtype='float')
        self.tool_transform = identity(4, dtype='float')
        self.global_rotation = identity(4, dtype='float')
        self.global_translation = zeros((3, 1), dtype='float')

        # move robot and joints to the initial position
        self.set_global_transform(
            global_rotation, global_translation
        )

    def global_transform(self):
        return concatenate(
            concatenate(self.global_rotation, self.global_translation, axis=1),
            float_([0, 0, 0, 1]).reshape((1, 4)), axis=0
        )

    def set_global_transform(self, rotation=None, translation=None):
        """Set the global transform for the overall arm assembly

        Args:
            rotation: [3x3] symmetric float array describing the rotation of
                      the robot.
            translation: [3x1] float array describing the x,y,z position of
                         the robot.
        """

        # TODO: Rotation matrix checking
        # Set input parameters to the correct type
        if rotation is not None:
            self.global_rotation = rotation
        if translation is not None:
            self.global_translation = translation
        self.move_joints(self.state)

    def move_joints(self, q):
        """Updates the transformation for each link of the robot and

        Args:
            q: a vector of joint states in order from the base to the top
        """

        # Check input
        self.check_q(q)

        # Apply all transforms one by one
        transform = self.global_transform()
        for k, link in enumerate(self.links):
            state_transform = dot(
                transform, link.state_transform(q[k])
            )
            self.link_transforms[:, :, k] = state_transform
            link.transform(
                rotation=state_transform[0:3, 0:3],
                translation=state_transform[0:3, 3]
            )
            transform = dot(state_transform, link.body_transform)

        # Set the tool transform
        self.tool_transform = transform

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
