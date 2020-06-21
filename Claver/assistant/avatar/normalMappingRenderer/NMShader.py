import os

from Claver.assistant.avatar.shaders.ShaderProgram import *
from Claver.assistant.avatar.entities.Light import Light
from Claver.assistant.avatar.toolbox.Math import createViewMatrix
from pyrr import Vector3, Vector4, matrix44


class NMShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "nmVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "nmFragmentShader.glsl")

    __MAX_LIGHTS = 4

    def __init__(self, camera):
        self.__camera = camera
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoordinates")
        super().bindAttribute(2, "normal")
        super().bindAttribute(3, "tangent")

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.__location_shineDamper = super().getUniformLocation("shineDamper")
        self.__location_reflectivity = super().getUniformLocation("reflectivity")
        self.__location_skyColour = super().getUniformLocation("skyColour")
        self.__location_numberOfRows = super().getUniformLocation("numberOfRows")
        self.__location_offset = super().getUniformLocation("offset")
        self.__location_plane = super().getUniformLocation("plane")
        self.__location_modelTexture = super().getUniformLocation("modelTexture")
        self.__location_normalMap = super().getUniformLocation("normalMap")

        self.__location_attenuation = []
        self.__location_lightPositionEyeSpace = []
        self.__location_lightColour = []
        for i in range(self.__MAX_LIGHTS):
            self.__location_lightPositionEyeSpace.append(super().getUniformLocation("lightPositionEyeSpace[{}]".format(i)))
            self.__location_lightColour.append(super().getUniformLocation("lightColour[{}]".format(i)))
            self.__location_attenuation.append(super().getUniformLocation("attenuation[{}]".format(i)))

    def connectTextureUnits(self):
        super().loadInt(self.__location_modelTexture, 0)
        super().loadInt(self.__location_normalMap, 1)


    def loadClipPlane(self, plane):
        super().load4DVector(self.__location_plane, plane)

    def loadNumberOfRows(self, numberOfRows):
        super().loadFloat(self.__location_numberOfRows, numberOfRows)

    def loadOffset(self, x, y):
        super().load2DVector(self.__location_offset, (x, y))

    def loadSkyColour(self, r, g, b):
        super().loadVector(self.__location_skyColour, (r, g, b))

    def loadShineVariables(self, damper, reflectivity):
        super().loadFloat(self.__location_shineDamper, damper)
        super().loadFloat(self.__location_reflectivity, reflectivity)

    def loadLights(self, lights):
        for i in range(self.__MAX_LIGHTS):
            if i < len(lights):
                super().loadVector(self.__location_lightPositionEyeSpace[i], self.getEyeSpacePosition(lights[i], self.__camera.getViewMatrix()))
                super().loadVector(self.__location_lightColour[i], lights[i].getColour())
                super().loadVector(self.__location_attenuation[i], lights[i].getAttenuation())
            else:
                super().loadVector(self.__location_lightPositionEyeSpace[i], (0.0, 0.0, 0.0))
                super().loadVector(self.__location_lightColour[i], (0.0, 0.0, 0.0))
                super().loadVector(self.__location_attenuation[i], (1.0, 0.0, 0.0))


    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self):
        super().loadMatrix(self.__location_viewMatrix, self.__camera.getViewMatrix())

    def getEyeSpacePosition(self, light, viewMatrix):
        position = light.getPosition()
        eyeSpacePos = Vector4((position[0], position[1], position[2], 1.0))
        eyeSpacePos = matrix44.apply_to_vector(viewMatrix, eyeSpacePos)
        return Vector3((eyeSpacePos[0], eyeSpacePos[1], eyeSpacePos[2]))
