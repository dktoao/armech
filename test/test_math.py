## test_math.py
#
# Test function for making sure all the robot math is correct
#

from numpy.testing import assert_array_almost_equal

from armech.demo.robot import Simple3DOF

def test_simple3dof_forward_kinematics():

    # get the robot
    robot = Simple3DOF()

    # Test 1
    q = [0, 0, 0]
    end = [
        [1.0000,  0.0000,  0.0000,  0.7500],
        [0.0000,  0.0000, -1.0000,  0.0400],
        [0.0000,  1.0000,  0.0000,  0.0000],
        [0.0000,  0.0000,  0.0000,  1.0000],
    ]

    assert_array_almost_equal(
        robot.get_tool_trans(q), end, 4
    )