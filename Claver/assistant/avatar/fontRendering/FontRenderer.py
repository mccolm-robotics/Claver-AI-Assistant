from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.fontRendering.FontShader import FontShader

class FontRenderer:

    def __init__(self):
        self.__shader = FontShader()

    def render(self, texts):
        self.__prepare()
        for font in texts:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, font.getTextureAtlas())
            for text in texts[font]:
                self.__renderText(text)
        self.__endRendering()

    def cleanUp(self):
        self.__shader.cleanUp()

    def __prepare(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        self.__shader.start()

    def __renderText(self, text):
        glBindVertexArray(text.getMesh())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        self.__shader.loadColour(text.getColour())
        self.__shader.loadTranslation(text.getPosition())
        glDrawArrays(GL_TRIANGLES, 0, int(text.getVertexCount()))
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindVertexArray(0)

    def __endRendering(self):
        self.__shader.stop()
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)


