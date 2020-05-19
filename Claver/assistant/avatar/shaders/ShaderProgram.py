from abc import ABC, abstractmethod
# https://www.python-course.eu/python3_abstract_classes.php
# https://docs.python.org/3/library/abc.html

class ShaderProgram(ABC):
    def __init__(self, vertexFile, fragmentFile):
        super().__init__()
        self.vertex_shader = loadShader(vertexFile, GL_VERTEX_SHADER)
        self.fragment_shader = loadShader(fragmentFile, GL_FRAGMENT_SHADER)
        self.__programID = compileProgram(vertex_shader, fragment_shader)
        # glValidateProgram(self.programID)

    @abstractmethod
    def getAllUniformLocations(self):
        pass

    def getUniformLocation(self, uniformName):
        return glGetUniformLocation(self.programID, uniformName)

    def start(self):
        glUseProgram(self.programID)

    @abstractmethod
    def bindAttributes(self):
        pass

    def bindAttribute(self, attribute, variableName):
        glBindAttribLocation(self.programID, attribute, variableName)

    def loadFloat(self, location, value):
        glUniform1f(location, value)

    def loadInt(self, location, value):
        glUniform1i(location, value)

    def loadVector(self, location, vector):
        glUniform3f(location, vector[0], vector[1], vector[2])

    def load2DVector(self, location, vector):
        glUniform2f(location, vector[0], vector[1])


    def loadBoolean(self, location, value):
        toLoad = 0
        if value:
            toLoad = 1
        glUniform1f(location, toLoad)

    def loadMatrix(self, location, matrix):
        glUniformMatrix4(location, false, matrix)


    def stop(self):
        glUseProgram(0)

    def cleanUp(self):
        self.stop()
        glDeleteProgram(self.programID)


    # file -> name of shader source code
    # type -> GL_VERTEX_SHADER or GL_FRAGMENT_SHADER
    def loadShader(file, type):
        while .... (code for loading contents of a file)
            shaderSource = file contents

        shader = compileShader(shaderSource, type)
        # Check to see if shader compiled successfully?

        return shader
