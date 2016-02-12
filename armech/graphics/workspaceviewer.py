# workspaceviewer.py
#
# Classes for viewing and navigating the workspace in 3D

from numpy import max, concatenate, absolute
from OpenGL.GL import glTranslatef, glRotatef, glClear, glEnable, glLightfv, \
    glColorMaterial, glCullFace, \
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LIGHTING, GL_LIGHT0, \
    GL_POSITION, GL_COLOR_MATERIAL, GL_FRONT, GL_AMBIENT_AND_DIFFUSE, \
    GL_CULL_FACE, GL_BACK, GL_DEPTH_TEST
from OpenGL.GLU import gluPerspective
import pygame
from pygame import display, time
from pygame.locals import DOUBLEBUF, OPENGL, QUIT

from armech.graphics.workspace import Workspace


class BaseViewer:
    """
    Basic viewer that provides simple initial_view and update_view functions
    that can be overwritten by subclasses to get more advanced functionality
    """
    # Update at 30 frames per second
    UPDATE_PERIOD = 1000//30

    def __init__(self, workspace):
        """
        Create a BaseViewer with the given workspace
        :param workspace: a Workspace object that has the desired elements for
        viewing
        :return: BaseViewer object
        """

        # Make sure that the input is a Workspace
        if isinstance(workspace, Workspace):
            self.workspace = workspace
        else:
            raise ValueError(
                'BaseViewer requires a Workspace object at initialization'
            )

        # Set up the callback dictionary for event handling
        self.callback_dict = {}
        # Flag to stop callbacks when and exit is occurring
        self.exit_flag = False

    def register_callback(self, event_type, event_key, function):
        """ Registers a callback function to the Viewer.

        Registers a callback function to be called when a pygame event occurs
        that matches 'type' and 'key'. All callbacks will be called in the
        'update_view' function. All functions registered should not take
        any arguments.

        Args:
            event_type: pygame event.type value to trigger callback
            event_key: pygame event.key value to trigger the callback
            function: callback function to register
        """
        if (event_type, event_key) not in self.callback_dict.keys():
            self.callback_dict[(event_type, event_key)] = [function]
        else:
            self.callback_dict[(event_type, event_key)].append(function)

    def initial_view(self):
        """
        Sets the initial view of the workspace using the glRotatef and
        glTranslatef functions.
        """

        # Set the the view distance based on the workspace size
        ws_max_dimension = max(absolute(concatenate(
            (
                self.workspace.bounds_x,
                self.workspace.bounds_y,
                self.workspace.bounds_z,
             )
        )))
        glTranslatef(0.0, 0.0, -3.0*ws_max_dimension)

        # Rotate the view
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        glRotatef(30.0, 0.0, 0.0, 1.0)

        # Move up to see the room
        glTranslatef(0.0, 0.0, -self.workspace.bounds_z[1] / 2.0)

    # TODO: Update this method to use the callback dict
    @staticmethod
    def update_view(**kwargs):
        """
        Function that updates the view for each frame. Override this function
        when inheriting this class to get different response to user input

        :param events: events object from the main loop
        :param rate: degrees per frame to rotate

        Note:
            If overriding this function, make sure that it only takes **kwargs
            as an argument.
        """

        # Get rate or set default
        rate = kwargs.get('rate', 0.4)

        # Rotate view
        glRotatef(rate, 0.0, 0.0, 1.0)

    def do_callbacks(self, events):
        """
        Get callbacks that match the event type and key and call them

        Args:
            events: events from the program main loop
        """
        for event in events.get():
            # Try to get the function from the callbacks dictionary
            try:
                callbacks = self.callback_dict[(event.type, event.key)]
            except KeyError:
                callbacks = []

            for callback in callbacks:
                callback()

    def cb_quit(self):
        """
        Callback function to quit the pygame instance and close all windows
        """
        pygame.quit()
        self.exit_flag = True

    def show(self, window_size=(800, 600), **kwargs):
        """
        Open a window showing the scene.
        :param window_size: (x, y) size of the viewing window in pixels
        :param kwargs: kwargs to pass to the update function
        """

        # Initialize the graphics window
        pygame.init()
        display.set_mode(window_size, DOUBLEBUF | OPENGL)

        # Initialize OpenGL
        gluPerspective(45, (window_size[0]/window_size[1]), 0.1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        # Initialize lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        # Place the light
        glLightfv(GL_LIGHT0, GL_POSITION, self.workspace.position_light)

        # Display the workspace
        self.initial_view()
        self.workspace.render_all()

        # Start event loop
        pygame_exit = False
        while not self.exit_flag:
            events = pygame.event.get()
            self.do_callbacks(events)
            self.update_view(**kwargs)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.workspace.render_all()
            display.flip()
            time.wait(self.UPDATE_PERIOD)


# TODO: add a WorkspaceViewer class that accepts user input to rotate view
