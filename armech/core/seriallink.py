# seriallink.py
#
# Implementation of a robotic arm that is a series of links, hence the name
# serial link robot. Provides functions for forward kinematics, inverse
# kinematics, and dynamics calculations.

from numpy import identity

class SerialLink:

    def __init__(self, links, base=None):
        """
        A serial link robot representation
        :param links: a list of Link classes to create the robot structure
        :param base: the base of the robot which relates the serial link
        structure to it's place in the environment.
        :return: A SerialLink robot object
        """

        self.links = links
        self.base = base

    def move_joints(self, q):
        """
        Updates the configuration of the robot
        Args:
            q: a vector of joint states in order from the base to the top
        """

        # Make sure the correct input is given
        if len(q) != len(self.links)
            raise IndexError(
                    'The number of element in q is not equal to the number'
                    'of links'
            )

        # Apply all transforms one by one
        global_transform = identity(4)
        for link in self.links

            link.transform()