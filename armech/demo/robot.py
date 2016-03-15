## robot.py
#
# Robot classes derived from the SerialLink class with specific configurations
# and geometries. For demonstration and testing purposes

# Package imports
from os.path import dirname, realpath, join
from numpy import pi

# Local imports
from armech.core.seriallink import SerialLink
from armech.core.linkdh import LinkDH
from armech.config import JOINT_REVOLUTE
from armech.graphics.graphicalbody import GraphicalBody


# Get the path to the cad directory
CAD_DIR = join(dirname(realpath(__file__)), 'cad')

class Simple3DOF(SerialLink):
    """A simple 3 degree of freedom robot class that can be used for testing
    and demonstration purposes.

    DH Table:
    -------------------------------------------------------------------
    |i    |a_i (mm)      |alpha_i (rad) |d_i (mm)      |theta_i (deg) |
    -------------------------------------------------------------------
    |0    |0             |pi/2          |0             |0             |
    |1    |400           |0             |40            |0             |
    |2    |350           |0             |-40           |0             |
    -------------------------------------------------------------------
    """

    def __init__(self, global_transform=None):
        """Get and instance of Simple3DOF robot."""

        # Create links
        base = GraphicalBody()
        link1 = LinkDH(JOINT_REVOLUTE, 0, pi/2, 0, 0)
        link2 = LinkDH(JOINT_REVOLUTE, 0.4, 0, 0.04, 0)
        link3 = LinkDH(JOINT_REVOLUTE, 0.35, 0, -0.08, 0)

        # Load graphics for each link
        obj_dir = join(CAD_DIR, 'simple3dof', 'obj')
        base.load_obj(join(obj_dir, 'base.obj'), [0.5, 0.5, 0.5])
        link1.load_obj(join(obj_dir, 'link1.obj'), [1.0, 0.0, 0.0])
        link2.load_obj(join(obj_dir, 'link2.obj'), [0.0, 1.0, 0.0])
        link3.load_obj(join(obj_dir, 'link3.obj'), [0.0, 0.0, 1.0])

        # Initialize the SerialLink super class
        super(Simple3DOF, self).__init__(
            [link1, link2, link3], base, global_transform
        )
