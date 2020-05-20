import sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from abc import ABC, abstractmethod
# https://www.python-course.eu/python3_abstract_classes.php
# https://docs.python.org/3/library/abc.html

class ShaderProgram(ABC):
    def __init__(self, vertexFile, fragmentFile):
        super().__init__()
        vertex_shader = self.loadShader(vertexFile, GL_VERTEX_SHADER)
        fragment_shader = self.loadShader(fragmentFile, GL_FRAGMENT_SHADER)
        self.__programID = compileProgram(vertex_shader, fragment_shader)

    def start(self):
        glUseProgram(self.__programID)

    def stop(self):
        glUseProgram(0)

    def cleanUp(self):
        self.stop()
        glDeleteProgram(self.__programID)

    @abstractmethod
    def bindAttributes(self):
        pass

    def bindAttribute(self, attribute, variableName):
        glBindAttribLocation(self.__programID, attribute, variableName)

    @staticmethod
    def loadShader(fileName, type):
        with open(fileName) as file:
            shaderSource = file.read()
        shaderID = compileShader(shaderSource, type)
        if glGetShaderiv(shaderID, GL_COMPILE_STATUS) == GL_FALSE:
            print(glGetShaderInfoLog(shaderID, 500))
            print("Error: Could not compile shader", file=sys.stderr)
        return shaderID