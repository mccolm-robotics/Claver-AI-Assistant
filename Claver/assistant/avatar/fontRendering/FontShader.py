import os
from Claver.assistant.avatar.shaders.ShaderProgram import ShaderProgram


class FontShader(ShaderProgram):
    __THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    __VERTEX_FILE = os.path.join(__THIS_FOLDER, "fontVertexShader.glsl")
    __FRAGMENT_FILE = os.path.join(__THIS_FOLDER, "fontFragmentShader.glsl")

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def getAllUniformLocations(self):
        self.__location_colour = super().getUniformLocation("colour")
        self.__location_translation = super().getUniformLocation("translation")

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoords")

    def loadColour(self, colour):
        super().loadVector(self.__location_colour, colour)

    def loadTranslation(self, translation):
        super().load2DVector(self.__location_translation, translation)
