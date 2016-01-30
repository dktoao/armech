# lighting.py
#
# Messing around with lighting in OpenGL

from numpy import int_, float_, sqrt
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Create a tetrahedron
TET1_VERTICES = float_((
    (0.0, 0.0, 0.0),
    (0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0),
    (1.0, 0.0, 0.0),
))

TET1_NORMALS = float_((
    (1/sqrt(3), 1/sqrt(3), 1/sqrt(3)),
    (0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0),
    (1.0, 0.0, 0.0),
))

TET1_FACES = int_((
    (0, 1, 2),
    (0, 3, 1),
    (0, 2, 3),
    (1, 3, 2),
))


# Function to draw the first tetrahedron
def tet1():
    glColor3fv((1.0, 0.0, 0.0))
    glBegin(GL_TRIANGLES)
    for face in TET1_FACES:
        for idx_vertex in face:
            glVertex3fv(TET1_VERTICES[idx_vertex, :])
    glEnd()


def main():
    pygame.init()
    window = (800, 600)
    pygame.display.set_mode(window, DOUBLEBUF|OPENGL)

    gluPerspective(45, (window[0]/window[1]), 0.1, 50.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(-5.0, 0.0, -5.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        tet1()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
