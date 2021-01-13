import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

X = 0.52573111212
Z = 0.85065080835

vertices = (
    (-X, 0, Z),
    (X, 0, Z),
    (-X, 0, -Z),
    (X, 0, -Z),
    (0, Z, X),
    (0, Z, -X),
    (0, -Z, X),
    (0, -Z, -X),
    (Z, X, 0),
    (-Z, X, 0),
    (Z, -X, 0),
    (-Z, -X, 0)
    )

triangles = (
    (0,4,1),
    (0,9,4),
    (9,5,4),
    (4,5,8),
    (4,8,1),
    (8,10,1),
    (8,3,10),
    (5,3,8),
    (5,2,3),
    (2,7,3),
    (7,10,3),
    (7,6,10),
    (7,11,6),
    (11,0,6),
    (0,1,6),
    (6,1,10),
    (9,0,11),
    (9,11,2),
    (9,2,5),
    (7,2,11)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

def icosahedron():
    glBegin(GL_TRIANGLES)
    for triangle in triangles:
        i = 0
        for vertex in triangle:
            i += 1
            glColor3fv(colors[i])
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pg.init()
    display = (1280, 720)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        icosahedron()
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()