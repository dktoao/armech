# workspace.py
#
# Workspace object that is a rectangular room which can be populated with
# robots, graspable objects and obstacles.

from OpenGL.GL import glClear, glBegin, glEnd, \
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_TRIANGLES, GL_LINES

from armech.graphics.graphicalbody import GraphicalBody
from armech.graphics.shapes import Box
from armech.core.seriallink import SerialLink


class Workspace(Box):

    def __init__(self, bounds_x, bounds_y, bounds_z,
                 face_color=(0.0, 1.0, 0.0),
                 edge_color=(0.2, 0.2, 0.2)):
        """
        Create a workspace object
        :param bounds_x: 1x2 array of the lower and upper bounds of the
        workspace's "x" dimension
        :param bounds_y: 1x2 array of the lower and upper bounds of the
        workspace's "y" dimension
        :param bounds_z: 1x2 array of the lower and upper bounds of the
        workspace's "z" dimension
        :param face_color: 1x3 array for the face color
        :param edge_color: 1x3 array for the face color
        :return: A Workspace object
        """

        # Initialize Box
        super(Workspace, self).__init__(bounds_x, bounds_y, bounds_z, face_color, edge_color, False)

        # Dictionaries of objects in the workspace
        self.obstacles = {}
        self.graspable_objects = {}
        self.robots = {}

        # Light position
        position_x_light = (bounds_x[0] + bounds_x[0])/2.0
        position_y_light = (bounds_y[0] + bounds_y[0])/2.0
        position_z_light = (bounds_z[0] + bounds_z[0])/2.0
        self.position_light = (
            position_x_light,
            position_y_light,
            position_z_light,
            0.0,
        )

    def add_obstacle(self, name, obstacle):
        """
        Adds an obstacle to the scene, can be accessed by name
        :param name: string, name given to the object
        :param obstacle: GraphicalBody object to add to the scene
        """

        # Check that the obstacle is a GraphicalBody
        if not isinstance(obstacle, GraphicalBody):
            raise ValueError(
                'The obstacle must be an instance of GraphicalBody'
            )

        # Add the obstacle to the obstacles dictionary
        self.obstacles[name] = obstacle

    def remove_obstacle(self, name):
        """
        Removes an obstacle from the workspace
        :param name: name of the obstacle to remove
        """
        self.obstacles.pop(name)

    def add_graspable_object(self, name, graspable_object):
        """
        Adds a graspable object to the scene that the robot can pickup and
        manipulate.
        :param name: string, name of the object
        :param graspable_object: RigidBody or GraphicalBody to be picked up
        """

        # Check that the object is a GraphicalBody or RigidBody
        if not isinstance(graspable_object, GraphicalBody):
            raise ValueError(
                'The object must be either an instance of GraphicalBody or '
                'RigidBody'
            )

        # Add the graspable object to the dictionary
        self.graspable_objects[name] = graspable_object

    def remove_graspable_object(self, name):
        """
        Removes a graspable object from the workspace
        :param name: name of the graspable object to remove
        """
        self.graspable_objects.pop(name)

    def add_robot(self, name, robot):
        """
        Adds a robot to the workspace
        :param name: Name of the robot
        :param robot: SerialLink object, Robot object to place in workspace
        """

        # Check that the object is a SerialLink object
        if not isinstance(robot, SerialLink):
            raise ValueError(
                'The robot must be an instance of the SerialLink class'
            )

        # Add the robot to the workspace
        self.robots[name] = robot

    def remove_robot(self, name):
        """
        Removes a robot from the workspace
        :param name: name of the robot to remove
        """
        self.robots.pop(name)

    def render_all(self):
        """
        Renders all the objects in the workspace to an OpenGL canvas
        """

        # Clear OpenGL
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render all faces
        glBegin(GL_TRIANGLES)
        self.render_faces()
        for obstacle in self.obstacles.values():
            obstacle.render_faces()
        for graspable_object in self.graspable_objects.values():
            graspable_object.render_faces()
        for robot in self.robots.values():
            robot.render_faces()
        glEnd()

        # Render all edges
        glBegin(GL_LINES)
        self.render_edges()
        for obstacle in self.obstacles.values():
            obstacle.render_edges()
        for graspable_object in self.graspable_objects.values():
            graspable_object.render_edges()
        for robot in self.robots.values():
            robot.render_edges()
        glEnd()
