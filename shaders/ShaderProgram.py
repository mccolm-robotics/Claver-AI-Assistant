from abc import ABC, abstractmethod
# https://www.python-course.eu/python3_abstract_classes.php
# https://docs.python.org/3/library/abc.html

class ShaderProgram(ABC):
    def __init__(self, vertexFile, fragmentFile):
        super().__init__()
        self.vertex_shader = loadShader(vertexFile, GL_VERTEX_SHADER)
        self.fragment_shader = loadShader(fragmentFile, GL_FRAGMENT_SHADER)
        self.programID = compileProgram(vertex_shader, fragment_shader)
        # glValidateProgram(self.programID)

    def start(self):
        glUseProgram(self.programID)

    @abstractmethod
    def bindAttributes(self):
        pass

    def bindAttribute(self, attribute, variableName):
        glBindAttribLocation(self.programID, attribute, variableName)

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
