# test_workspace.py
#
# Tests to insure that the Workspace object is functioning

import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT
from pygame import display
from OpenGL.GL import glTranslatef, glRotate, glClear, glBegin, glEnd, \
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LINES, GL_TRIANGLES
from OpenGL.GLU import gluPerspective

from armech.graphics.workspace import Workspace


# Get the workspace object
ws = Workspace((-1, 1), (-1, 1), (0, 2))

# initialize pygame and OpenGL
pygame.init()
window_size = (800, 600)
display.set_mode(window_size, DOUBLEBUF | OPENGL)
gluPerspective(45, (window_size[0]/window_size[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5.0)
glRotate(-90, 1, 0, 0)

# Start event loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    glRotate(1, 1, 1, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # draw the faces
    glBegin(GL_TRIANGLES)
    ws.render_faces()
    glEnd()
    # draw the edges
    glBegin(GL_LINES)
    ws.render_edges()
    glEnd()
    pygame.display.flip()
    pygame.time.wait(10)