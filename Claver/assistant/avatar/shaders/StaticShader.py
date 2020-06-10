import os

from Claver.assistant.avatar.shaders.ShaderProgram import *
from Claver.assistant.avatar.entities.Light import Light
from Claver.assistant.avatar.toolbox.Math import createViewMatrix


class StaticShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "vertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "fragmentShader.txt")

    __MAX_LIGHTS = 4

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoords")
        super().bindAttribute(2, "normal")

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        # self.__location_lightPosition = super().getUniformLocation("lightPosition")
        # self.__location_lightColour = super().getUniformLocation("lightColour")
        self.__location_shineDamper = super().getUniformLocation("shineDamper")
        self.__location_reflectivity = super().getUniformLocation("reflectivity")
        self.__location_useFakeLighting = super().getUniformLocation("useFakeLighting")
        self.__location_skyColour = super().getUniformLocation("skyColour")
        self.__location_numberOfRows = super().getUniformLocation("numberOfRows")
        self.__location_offset = super().getUniformLocation("offset")

        self.__location_lightPosition = []
        self.__location_lightColour = []
        for i in range(self.__MAX_LIGHTS):
            self.__location_lightPosition.append(super().getUniformLocation("lightPosition[{}]".format(i)))
            self.__location_lightColour.append(super().getUniformLocation("lightColour[{}]".format(i)))


    def loadNumberOfRows(self, numberOfRows):
        super().loadFloat(self.__location_numberOfRows, numberOfRows)

    def loadOffset(self, x, y):
        super().load2DVector(self.__location_offset, (x, y))

    def loadSkyColour(self, r, g, b):
        super().loadVector(self.__location_skyColour, (r, g, b))

    def loadFakeLightingVariable(self, useFake):
        super().loadBoolean(self.__location_useFakeLighting, useFake)

    def loadShineVariables(self, damper, reflectivity):
        super().loadFloat(self.__location_shineDamper, damper)
        super().loadFloat(self.__location_reflectivity, reflectivity)

    def loadLights(self, lights):
        for i in range(self.__MAX_LIGHTS):
            if i < len(lights):
                super().loadVector(self.__location_lightPosition[i], lights[i].getPosition())
                super().loadVector(self.__location_lightColour[i], lights[i].getColour())
            else:
                super().loadVector(self.__location_lightPosition[i], (0.0, 0.0, 0.0))
                super().loadVector(self.__location_lightColour[i], (0.0, 0.0, 0.0))


    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
