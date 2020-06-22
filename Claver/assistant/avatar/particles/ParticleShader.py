import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class ParticleShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "particleVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "particleFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def getAllUniformLocations(self):
        self.__location_modelViewMatrix = super().getUniformLocation("modelViewMatrix")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")

    def bindAttributes(self):
        super().bindAttribute(0, "position")

    def loadModelViewMatrix(self, modelView):
        super().loadMatrix(self.__location_modelViewMatrix, modelView)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)
