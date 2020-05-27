import os

from Claver.assistant.avatar.entities.Light import Light
from Claver.assistant.avatar.toolbox.Math import createViewMatrix
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram

class TerrainShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "TerrainVertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "TerrainFragmentShader.txt")

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
        self.__location_lightPosition = super().getUniformLocation("lightPosition")
        self.__location_lightColour = super().getUniformLocation("lightColour")
        self.__location_shineDamper = super().getUniformLocation("shineDamper")
        self.__location_reflectivity = super().getUniformLocation("reflectivity")
        self.__location_skyColour = super().getUniformLocation("skyColour")
        self.__location_backgroundTexture = super().getUniformLocation("backgroundTexture")
        self.__location_rTexture = super().getUniformLocation("rTexture")
        self.__location_gTexture = super().getUniformLocation("gTexture")
        self.__location_bTexture = super().getUniformLocation("bTexture")
        self.__location_blendMap = super().getUniformLocation("blendMap")

    def connectTextureUnits(self):
        super().loadInt(self.__location_backgroundTexture, 0)
        super().loadInt(self.__location_rTexture, 1)
        super().loadInt(self.__location_gTexture, 2)
        super().loadInt(self.__location_bTexture, 3)
        super().loadInt(self.__location_blendMap, 4)

    def loadSkyColour(self, r, g, b):
        super().loadVector(self.__location_skyColour, (r, g, b))

    def loadShineVariables(self, damper, reflectivity):
        super().loadFloat(self.__location_shineDamper, damper)
        super().loadFloat(self.__location_reflectivity, reflectivity)

    def loadLight(self, light):
        super().loadVector(self.__location_lightPosition, light.getPosition())
        super().loadVector(self.__location_lightColour, light.getColour())


    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
