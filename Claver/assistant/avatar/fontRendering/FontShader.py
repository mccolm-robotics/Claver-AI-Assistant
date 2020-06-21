import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class FontShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "fontVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "fontFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def getAllUniformLocations(self):
        pass

    def bindAttributes(self):
        pass