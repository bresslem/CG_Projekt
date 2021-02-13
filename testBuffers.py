# import pygame as pg
# from pygame.locals import *

import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo

import numpy
import sys
import ctypes

vertexShaderSource = """#version 330 core
uniform mat4 cProjectionMatrix;
uniform mat4 cModelviewMatrix;
in vec4 in_Position;

void main()
{
    gl_Position = cProjectionMatrix * cModelviewMatrix * in_Position;
} """


fragmentShaderSource = """#version 330 core
out vec4 out_color;
void main()
{
  out_color = vec4( 1.0, 1.0, 1.0, 1.0);
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

def main():

    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1024, 720, "Icosahedron", None, None)

    glfw.make_context_current(window)

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

    if not glGetProgramiv(shaderProgram, GL_LINK_STATUS):
        print(glGetProgramInfoLog(shaderProgram))
        raise RuntimeError('Linking Error')

    glDeleteShader(vertexShader)
    glDeleteShader(fragmentShader)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)

    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER, triangles, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
    # glBindBuffer(GL_ARRAY_BUFFER, 0)


    while (not glfw.window_should_close(window)):
        if (glfw.get_key(window, glfw.KEY_ESCAPE) is glfw.PRESS):
            glfw.set_window_should_close(window, True)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(shaderProgram)
        glBindVertexArray(VAO)

        glDrawElements(GL_TRIANGLES, 60, GL_UNSIGNED_INT, 0)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
