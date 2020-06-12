import os
from math import radians

import numpy as np
import pyrr
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram

class SkyboxShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "SkyboxVertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "SkyboxFragmentShader.txt")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)
        self.__ROTATE_SPEED = 1.0
        self.__rotation = 0

    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera, delta):
        matrix = camera.getViewMatrix()
        matrix.m41 = 0
        matrix.m42 = 0
        matrix.m43 = 0
        super().loadMatrix(self.__location_viewMatrix, matrix)

    def loadFogColour(self, r, g, b):
        super().loadVector(self.__location_fogColour, Vector3((r, g, b)))

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_fogColour = super().getUniformLocation("fogColour")

    def bindAttributes(self):
        super().bindAttribute(0, "position")
