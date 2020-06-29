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
        self.__location_texOffset1 = super().getUniformLocation("texOffset1")
        self.__location_texOffset2 = super().getUniformLocation("texOffset2")
        self.__location_texCoordInfo = super().getUniformLocation("texCoordInfo")

    def bindAttributes(self):
        super().bindAttribute(0, "position")

    def loadTextureCoordInfo(self, offset1, offset2, numRows, blend):
        super().load2DVector(self.__location_texOffset1, offset1)
        super().load2DVector(self.__location_texOffset2, offset2)
        super().load2DVector(self.__location_texCoordInfo, (numRows, blend))

    def loadModelViewMatrix(self, modelView):
        super().loadMatrix(self.__location_modelViewMatrix, modelView)

    def loadProjectionMatrix(self, matrix):
        super().loadMatrix(self.__location_projectionMatrix, matrix)
