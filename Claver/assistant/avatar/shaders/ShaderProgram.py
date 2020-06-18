import sys

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from abc import ABC, abstractmethod
# https://www.python-course.eu/python3_abstract_classes.php
# https://docs.python.org/3/library/abc.html

class ShaderProgram(ABC):
    def __init__(self, vertexFile, fragmentFile):
        super().__init__()
        vertex_shader = self.__loadShader(vertexFile, GL_VERTEX_SHADER)
        fragment_shader = self.__loadShader(fragmentFile, GL_FRAGMENT_SHADER)
        self.__programID = compileProgram(vertex_shader, fragment_shader)
        self.getAllUniformLocations()

    @abstractmethod
    def getAllUniformLocations(self):
        pass

    def getUniformLocation(self, uniformName):
        return glGetUniformLocation(self.__programID, uniformName)

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

    def loadFloat(self, location, value):
        glUniform1f(location, value)

    def loadInt(self, location, value):
        glUniform1i(location, value)

    def load4DVector(self, location, vector):
        glUniform4f(location, vector[0], vector[1], vector[2], vector[3])

    def loadVector(self, location, vector):
        glUniform3f(location, vector[0], vector[1], vector[2])

    def load2DVector(self, location, vector):
        glUniform2f(location, vector[0], vector[1])

    def loadBoolean(self, location, boolean):
        toLoad = 0
        if boolean:
            toLoad = 1
        glUniform1f(location, toLoad)

    def loadMatrix(self, location, matrix):
        glUniformMatrix4fv(location, 1, GL_FALSE, matrix)

    @staticmethod
    def __loadShader(fileName, type):
        with open(fileName) as file:
            shaderSource = file.read()
        shaderID = compileShader(shaderSource, type)
        if glGetShaderiv(shaderID, GL_COMPILE_STATUS) == GL_FALSE:
            print(glGetShaderInfoLog(shaderID, 500))
            print("Error: Could not compile shader", file=sys.stderr)
        return shaderID