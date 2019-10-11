from ctypes import *
import sys
import numpy as np
import math
import PIL
from PIL import Image

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from mathstuff import *

GL_VERTEX_SHADER = 0x8B31
GL_FRAGMENT_SHADER = 0x8B30
GL_COMPILE_STATUS = 0x8B81
GL_LINK_STATUS = 0x8B82
GL_INFO_LOG_LENGTH = 0x8B84


def glInit(x, y):
    screen = pygame.display.set_mode((x, y), HWSURFACE | OPENGL | DOUBLEBUF)
    glViewport(0, 0, x, y)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    viewport = glGetIntegerv(GL_VIEWPORT)

def readShader(source):
    file = open(source, 'r')
    data = file.read()
    # print(data)
    data = bytes(data, 'utf-8')
    file.close()
    return data

def compileShader(source, shaderType):
    shaderData = readShader(source)
    shader = glCreateShader(shaderType)
    source = c_char_p(shaderData)
    length = c_int(-1)
    glShaderSource(shader, shaderData)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))

    return shader

def compileProgram(vertex_source, fragment_source):
    vertexShader = None
    fragmentShader = None

    program = glCreateProgram()

    if vertex_source:
        vertexShader = compileShader(vertex_source, GL_VERTEX_SHADER)
        glAttachShader(program, vertexShader)
    if fragment_source:
        fragmentShader = compileShader(fragment_source, GL_FRAGMENT_SHADER)
        glAttachShader(program, fragmentShader)

    glLinkProgram(program)

    if vertexShader:
        glDeleteShader(vertexShader)
    if fragmentShader:
        glDeleteShader(fragmentShader)

    return program, vertexShader, fragmentShader

def main():
    pygame.init()
    glInit(1366, 768)
    glutInit()
    program, vertexShader, fragmentShader = compileProgram("vertex_shader.c", "fragment_shader.c")
    # glEnable(GL_DEPTH_TEST)
   
    UNIFORMS_LOCATIONS = {
            "projectionMatrix" : glGetUniformLocation(program, "projectionMatrix"),
            "modelMatrix" : glGetUniformLocation(program, "modelMatrix"),
            "viewMatrix" : glGetUniformLocation(program, "viewMatrix"),
            "atlas" : glGetUniformLocation(program, "atlas")
            }

    angle = 0

    cY = 1
    cX = 0
    cZ = 0
    rZ = 90

    img = pygame.image.load("sphere256.png")
    imgData = pygame.image.tostring(img, "RGB", 1)
    width, height = img.get_width(), img.get_height()

    glEnable(GL_POINT_SPRITE)
    glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)

    texture = glGenBuffers(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, imgData)

    glEnable(GL_TEXTURE_2D)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)

    deltaX = 0
    deltaY = 0
    deltaZ = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    deltaY = 0.1
                elif event.key == pygame.K_s:
                    deltaY = -0.1
                elif event.key == pygame.K_d:
                    deltaX = 0.1
                elif event.key == pygame.K_a:
                    deltaX = -0.1

                elif event.key == pygame.K_q:
                    # rZ -= 10
                    deltaZ = -0.1
                elif event.key == pygame.K_e:
                    # rZ += 10
                    deltaZ = 0.1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    deltaY = 0
                elif event.key == pygame.K_s:
                    deltaY = 0
                elif event.key == pygame.K_d:
                    deltaX = 0
                elif event.key == pygame.K_a:
                    deltaX = 0
                elif event.key == pygame.K_q:
                    deltaZ = 0
                elif event.key == pygame.K_e:
                    deltaZ = 0


        cY += deltaY
        cX -= deltaX
        cZ -= deltaZ

        '''
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    cY = 0
                elif event.key == pygame.K_d or event.key == pygame.K_a:
                    cX = 0
                elif event.key == pygame.K_q or event.key == pygame.K_e:
                     rZ = 0
        '''

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        eye = np.array([0.0, 0.0, 0.0])
        target = np.array([cX, cY, cZ])
        up = np.array([0.0, 0.0, 1.0])

        projectionMatrix = perspective(90.0, 1366.0 / 768.0, 0.1, 1000.0)
        viewMatrix = lookat(eye, target, up)
        viewMatrix = identity()
        modelMatrix = translate((cX, cZ, -3.0 + cY))
        modelMatrix *= rotate(rZ, (0.0, 1.0, 0.0))
        
        angle += 1.0

        glUseProgram(program)

        glUniformMatrix4fv(UNIFORMS_LOCATIONS["projectionMatrix"], 1, GL_TRUE,  projectionMatrix)
        glUniformMatrix4fv(UNIFORMS_LOCATIONS["modelMatrix"], 1, GL_TRUE, modelMatrix)        
        glUniformMatrix4fv(UNIFORMS_LOCATIONS["viewMatrix"], 1, GL_TRUE, viewMatrix)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(UNIFORMS_LOCATIONS["atlas"], 0)


        glDrawArrays(GL_POINTS, 0, width*height)
        
        pygame.display.flip()
        pygame.time.wait(1)



main()
