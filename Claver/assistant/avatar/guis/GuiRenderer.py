from OpenGL.GL import *
from Claver.assistant.avatar.renderEngine.Loader import Loader
from Claver.assistant.avatar.guis.GuiShader import GuiShader
from Claver.assistant.avatar.toolbox.Math import create2DTransformationMatrix

class GuiRenderer:
    def __init__(self, loader):
        positions = [-1, 1, -1, -1, 1, 1, 1, -1]
        self.__quad = loader.load2DToVAO(positions)
        self.__shader = GuiShader()

    def render(self, guis):
        self.__shader.start()
        glBindVertexArray(self.__quad.getVaoID())
        glEnableVertexAttribArray(0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        for gui in guis:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, gui.getTexture())
            matrix = create2DTransformationMatrix(gui.getPosition(), gui.getScale())
            self.__shader.loadTransformationMatrix(matrix)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.__quad.getVertexCount())
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def cleanUp(self):
        self.__shader.cleanUp()