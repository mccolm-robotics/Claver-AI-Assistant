import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class WaterShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "waterVertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "waterFragmentShader.txt")

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

    def connectTextureUnits(self):
        super().loadInt(self.__location_reflectionTexture, 0)
        super().loadInt(self.__location_refractionTexture, 1)

    def loadModelMatrix(self, matrix):
        super().loadMatrix(self.__location_modelMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
