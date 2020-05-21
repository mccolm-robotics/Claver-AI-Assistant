import os

from Claver.assistant.avatar.shaders.ShaderProgram import *
from Claver.assistant.avatar.toolbox.Math import createViewMatrix


class TestShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "testVertex.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "testFragment.txt")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        # super().bindAttribute(1, "textureCoords")

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")

    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = createViewMatrix(camera)
        super().loadMatrix(self.__location_viewMatrix, matrix)
