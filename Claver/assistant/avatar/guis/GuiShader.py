import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram

class GuiShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "GuiVertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "GuiFragmentShader.txt")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def loadTransformationMatrix(self, matrix):
        super().loadMatrix(self.__location_transformationMatrix, matrix)

    def getAllUniformLocations(self):
        self.__location_transformationMatrix = super().getUniformLocation("transformationMatrix")

    def bindAttributes(self):
        super().bindAttribute(0, "position")