## robot.py
#
# Robot classes derived from the SerialLink class with specific configurations
# and geometries. For demonstration and testing purposes

# Package imports
from numpy import pi

# Local imports
from armech.core.seriallink import SerialLink
from armech.core.linkdh import LinkDH
from armech.config import JOINT_REVOLUTE
from armech.graphics.graphicalbody import GraphicalBody


class Simple3DOF(SerialLink):
    """A simple 3 degree of freedom robot class that can be used for testing
    and demonstration purposes.

    DH Table:
    ---------------------------------------------------------------
    |i    |a_i (mm)     |alpha_i (deg)|d_i (mm)     |theta_i (deg)|
    ---------------------------------------------------------------
    |0    |0            |90           |0            |0            |
    |1    |400          |0            |40           |0            |
    |2    |350          |0            |-40          |0            |
    ---------------------------------------------------------------
    """

    def __init__(self):
        """Get and instance of Simple3DOF robot."""

        # Create links
        base = GraphicalBody()
        link0 = LinkDH(JOINT_REVOLUTE, 0, pi/2, 0, 0)
        link1 = LinkDH(JOINT_REVOLUTE, 0.4, 0, 0.04, 0)
        link2 = LinkDH(JOINT_REVOLUTE, 0.35, 0, -0.04, 0)

        # Initialize the SerialLink super class
        super(Simple3DOF, self).__init__([link0, link1, link2], base)

        # Load the graphics
        # TODO: implement the rest