import os

from Claver.assistant.avatar.entities.Light import Light
from Claver.assistant.avatar.toolbox.Math import createViewMatrix
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram

class TerrainShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "TerrainVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "TerrainFragmentShader.glsl")

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
        self.__location_skyColour = super().getUniformLocation("skyColour")
        self.__location_backgroundTexture = super().getUniformLocation("backgroundTexture")
        self.__location_rTexture = super().getUniformLocation("rTexture")
        self.__location_gTexture = super().getUniformLocation("gTexture")
        self.__location_bTexture = super().getUniformLocation("bTexture")
        self.__location_blendMap = super().getUniformLocation("blendMap")
        self.__location_plane = super().getUniformLocation("plane")

        self.__location_attenuation = []
        self.__location_lightPosition = []
        self.__location_lightColour = []
        for i in range(self.__MAX_LIGHTS):
            self.__location_lightPosition.append(super().getUniformLocation("lightPosition[{}]".format(i)))
            self.__location_lightColour.append(super().getUniformLocation("lightColour[{}]".format(i)))
            self.__location_attenuation.append(super().getUniformLocation("attenuation[{}]".format(i)))

    def loadClipPlane(self, plane):
        super().load4DVector(self.__location_plane, plane)

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

    def loadLights(self, lights):
        for i in range(self.__MAX_LIGHTS):
            if i < len(lights):
                super().loadVector(self.__location_lightPosition[i], lights[i].getPosition())
                super().loadVector(self.__location_lightColour[i], lights[i].getColour())
                super().loadVector(self.__location_attenuation[i], lights[i].getAttenuation())
            else:
                super().loadVector(self.__location_lightPosition[i], (0.0, 0.0, 0.0))
                super().loadVector(self.__location_lightColour[i], (0.0, 0.0, 0.0))
                super().loadVector(self.__location_attenuation[i], (1.0, 0.0, 0.0))

    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
