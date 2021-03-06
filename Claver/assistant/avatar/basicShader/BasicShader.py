import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class BasicShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "basicVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "basicFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")

    def getAllUniformLocations(self):
        self.__location_modelMatrix = super().getUniformLocation("modelMatrix")
        self.__location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")

    def loadModelMatrix(self, matrix):
        super().loadMatrix(self.__location_modelMatrix, matrix)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)

    def loadViewMatrix(self, camera):
        matrix = camera.getViewMatrix()
        super().loadMatrix(self.__location_viewMatrix, matrix)
