## link_tform_matrix.py
#
# Calculate the transform matrix for a single link from it's DH parameters:
# * a
# * alpha
# * d
# * theta

from sympy import symbols, Matrix, sin, cos, init_printing, pprint

# Initialize pretty printing
init_printing()

# DH Parameters of the link
a, alpha, d, theta = symbols(r'a alpha d theta')

# First, calculate the transform from the end of the last link to the first
# axis of the joint.
tform_1 = Matrix([
    [cos(theta),  sin(theta), 0, 0],
    [-sin(theta), cos(theta), 0, 0],
    [0,           0,          1, d],
    [0,           0,          0, 1],
])

# Second, calculate the transform from the axis of the joint to the end of
# the joint;
tform_2 = Matrix([
    [1, 0,           0,          a],
    [0, cos(alpha),  sin(alpha), 0],
    [0, -sin(alpha), cos(alpha), 0],
    [0, 0,           0,          1],
])

# Calculate the overall transform and display
tform = tform_1 * tform_2
pprint(tform)