import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class WaterShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "waterVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "waterFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")

    def getAllUniformLocations(self):
        self.__location_modelMatrix = super().getUniformLocation("modelMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.__location_reflectionTexture = super().getUniformLocation("reflectionTexture")
        self.__location_refractionTexture = super().getUniformLocation("refractionTexture")
        self.__location_dudvMap = super().getUniformLocation("dudvMap")
        self.__location_moveFactor = super().getUniformLocation("moveFactor")
        self.__location_cameraPosition = super().getUniformLocation("cameraPosition")
        self.__location_normalMap = super().getUniformLocation("normalMap")
        self.__location_lightColour = super().getUniformLocation("lightColour")
        self.__location_lightPosition = super().getUniformLocation("lightPosition")
        self.__location_depthMap = super().getUniformLocation("depthMap")

    def connectTextureUnits(self):
        super().loadInt(self.__location_reflectionTexture, 0)
        super().loadInt(self.__location_refractionTexture, 1)
        super().loadInt(self.__location_dudvMap, 2)
        super().loadInt(self.__location_normalMap, 3)
        super().loadInt(self.__location_depthMap, 4)

    def loadLight(self, sun):
        super().loadVector(self.__location_lightColour, sun.getColour())
        super().loadVector(self.__location_lightPosition, sun.getPosition())

    def loadMoveFactor(self, factor):
        super().loadFloat(self.__location_moveFactor, factor)

    def loadModelMatrix(self, matrix):
        super().loadMatrix(self.__location_modelMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
        super().loadVector(self.__location_cameraPosition, camera.getPosition())
