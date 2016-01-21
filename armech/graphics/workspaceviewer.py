# workspaceviewer.py
#
# Classes for viewing the workspace

from numpy import max, concatenate, absolute, int_
from OpenGL.GL import glTranslatef, glRotatef, glClear, \
        GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
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
            self._workspace = workspace
        else:
            raise ValueError(
                'BaseViewer requires a Workspace object at initialization'
            )

    def initial_view(self):
        """
        Sets the initial view of the workspace using the glRotatef and
        glTranslatef functions.
        """

        # Set the the view distance based on the workspace size
        ws_max_dimension = max(absolute(concatenate(
            (
                self._workspace.bounds_x,
                self._workspace.bounds_y,
                self._workspace.bounds_z,
             )
        )))
        glTranslatef(0.0, 0.0, -3.0*ws_max_dimension)

        # Rotate the view
        glRotatef(90.0, 1.0, 0.0, 0.0)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        glRotatef(30.0, 0.0, 0.0, 1.0)
        glRotatef(-30.0, 1.0, 0.0, 0.0)

    @staticmethod
    def update_view(events, **kwargs):
        """
        Function that updates the view for each frame
        :param events: events object from the main loop
        :param rate: degrees per frame to rotate
        """

        # Get rate or set default
        rate = kwargs.get('rate', 0.4)

        # Rotate view
        #glRotatef(rate, 0.0, 0.0, 1.0)

    def show(self, window_size=(800, 600), **kwargs):
        """
        Open a window showing the scene
        :param window_size: (x, y) size of the viewing window in pixels
        :param kwargs: kwargs to pass to the update function
        """

        # Initialize the graphics window
        pygame.init()
        display.set_mode(window_size, DOUBLEBUF | OPENGL)
        gluPerspective(45, (window_size[0]/window_size[1]), 0.1, 100.0)
        self.initial_view()

        # Display the workspace
        self._workspace.render_all()

        # Start event loop
        pygame_exit = False
        while not pygame_exit:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    pygame_exit = True

            if not pygame_exit:
                #glRotatef(0.5, 0.0, 0.0, 0.1)
                self.update_view(events, **kwargs)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                self._workspace.render_all()
                display.flip()
                time.wait(self.UPDATE_PERIOD)
            else:
                pygame.quit()

# TODO: add a WorkspaceViewer class that accepts user input to rotate view