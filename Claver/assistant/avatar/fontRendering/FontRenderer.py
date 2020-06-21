from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.fontRendering.FontShader import FontShader

class FontRenderer:

    def __init__(self):
        self.__shader = FontShader()

    def cleanUp(self):
        self.__shader.cleanUp()

    def prepare(self):
        pass

    def renderText(self, text):
        pass

    def endRendering(self):
        pass


