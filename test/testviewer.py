# testviewer.py
#
# WorkspaceViewer based classes that pass or raise errors depending on user
# input. These are for testing purposes only.

from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT
from OpenGL.GL import glColor3fv, glWindowPos2iv
from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13
from numpy import float_, int_
from ctypes import c_int

from armech.graphics.workspaceviewer import BaseViewer


class UserYesNoTestViewer(BaseViewer):
    """Viewer that accepts yes/no keys to determine if a test is passed."""

    def __init__(self, workspace, test_message):
        """Get a test viewer object.

        Args:
            test_message: Message that the user should respond with a Yes/No
                          answer to.
        """
        # Initialize the super BaseViewer class
        super(UserYesNoTestViewer, self).__init__(workspace)

        # Set the test_message variable
        self.test_message = test_message

        # Register new callbacks
        self.register_callback(KEYDOWN, K_LEFT, self.cb_fail_test)
        self.register_callback(KEYDOWN, K_RIGHT, self.cb_quit)

    @staticmethod
    def cb_fail_test():
        """Raise error and fail the test"""
        raise UserTestError('The test observer has failed the test')

    def update_view(self, **kwargs):
        """Display Message for the user to respond to"""

        # Call super class to rotate view
        super(UserYesNoTestViewer, self).update_view(**kwargs)

        # Print text to the screen
        glColor3fv(float_((1.0, 1.0, 1.0)))
        # User message
        glWindowPos2iv(int_((50, 50)))
        for c in (self.test_message + ' ( -> YES | <- NO )'):
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, c_int(ord(c)))


class UserTestError(Exception):
    """Error for user failing the class"""
    pass