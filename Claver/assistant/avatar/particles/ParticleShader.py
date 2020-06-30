import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class ParticleShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "particleVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "particleFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def getAllUniformLocations(self):
        self.__location_numberOfRows = super().getUniformLocation("numberOfRows")
        self.__location_projectionMatrix = super().getUniformLocation("projectionMatrix")

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "modelViewMatrix")     # Locations were set out in ParticleRenderer ln. 24
        super().bindAttribute(5, "texOffsets")
        super().bindAttribute(6, "blendFactor")

    def loadNumberOfRows(self, numberOfRows):
        super().loadFloat(self.__location_numberOfRows, numberOfRows)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)
