import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

# OpenGL.USE_ACCELERATE = False
# OpenGL.ERROR_CHECKING = False

import numpy
import sys

vertexShaderSource = """#version 150
uniform mat4  cProjectionMatrix;
uniform mat4  cModelviewMatrix;

in vec4 in_Position;

void main()
{
  gl_Position = cProjectionMatrix * cModelviewMatrix * in_Position;
} """


fragmentShaderSource = """#version 150
out vec4 out_color;
void main()
{
  out_color = vec4( 1.0, 0.0, 1.0, 1.0 );
}"""


X = 0.52573111212
Z = 0.85065080835

vertices = numpy.array(
    [-X, 0, Z,
    X, 0, Z,
    -X, 0, -Z,
    X, 0, -Z,
    0, Z, X,
    0, Z, -X,
    0, -Z, X,
    0, -Z, -X,
    Z, X, 0,
    -Z, X, 0,
    Z, -X, 0,
    -Z, -X, 0], dtype='float32')

triangles = numpy.array(
    [0,4,1,
     0,9,4,
     9,5,4,
     4,5,8,
     4,8,1,
     8,10,1,
     8,3,10,
     5,3,8,
     5,2,3,
     2,7,3,
     7,10,3,
     7,6,10,
     7,11,6,
     11,0,6,
     0,1,6,
     6,1,10,
     9,0,11,
     9,11,2,
     9,2,5,
     7,2,11], dtype='int16')


def icosahedron():
    vertices_r = vertices.reshape((12, 3))
    triangles_r = triangles.reshape((20, 3))
    glBegin(GL_TRIANGLES)
    for triangle in triangles_r:
        for vertex in triangle:
            glVertex3fv(vertices_r[vertex])
    glEnd()

def main():
    # glutInit(sys.argv)
    # glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    # glutCreateWindow('interactive')
    pg.init()
    display = (1280, 720)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 0)
    pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    print(glGetString(GL_VERSION))
    # err = glGetError()
    # if (err != GL_NO_ERROR):
    #     print('GLERROR: ', gluErrorString( err ))
    #     sys.exit()

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    glBindVertexArray(0)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, triangles, GL_DYNAMIC_DRAW)


    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertexShaderSource)
    glCompileShader(vertexShader)

    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragmentShaderSource)
    glCompileShader(fragmentShader)

    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glUseProgram(shaderProgram)
        glBindVertexArray(VAO)
        glDrawElements(GL_TRIANGLES, 12, GL_UNSIGNED_INT, 0)
        pg.display.flip()
        pg.time.wait(10)

    glDeleteShader(vertexShader)
    glDeleteShader(fragmentShader)

if __name__ == "__main__":
    main()