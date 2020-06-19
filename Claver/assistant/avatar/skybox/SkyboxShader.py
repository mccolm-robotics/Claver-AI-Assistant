import os
from math import radians

import numpy as np
import pyrr
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram

class SkyboxShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "SkyboxVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "SkyboxFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_fogColour = super().getUniformLocation("fogColour")
        self.__location_cubeMap = super().getUniformLocation("cubeMap")
        self.__location_cubeMap2 = super().getUniformLocation("cubeMap2")
        self.__location_blendFactor = super().getUniformLocation("blendFactor")

    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        # matrix.m41 = 0
        # matrix.m42 = 0
        # matrix.m43 = 0
        super().loadMatrix(self.__location_viewMatrix, matrix)

    def loadFogColour(self, r, g, b):
        super().loadVector(self.__location_fogColour, Vector3((r, g, b)))

    def connectTextureUnits(self):
        super().loadInt(self.__location_cubeMap, 0)
        super().loadInt(self.__location_cubeMap2, 1)

    def loadBlendFactor(self, blend):
        super().loadFloat(self.__location_blendFactor, blend)

