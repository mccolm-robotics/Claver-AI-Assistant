import os

from Claver.assistant.avatar.shaders.ShaderProgram import *


class StaticShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "vertexShader.txt")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "fragmentShader.txt")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoords")

    def getAllUniformLocations(self):
        super().getUniformLocation() tutorial # 7
