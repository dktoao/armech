# seriallink.py
#
# Implementation of a robotic arm that is a series of links, hence the name
# serial link robot. Provides functions for forward kinematics, inverse
# kinematics, and dynamics calculations.


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