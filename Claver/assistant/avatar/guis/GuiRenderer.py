from OpenGL.GL import *
from Claver.assistant.avatar.renderEngine.Loader import Loader

class GuiRenderer:
    def __init__(self, loader):
        positions = [-1, 1, -1, -1, 1, 1, 1, -1]
        self.__quad = loader.load2DToVAO(positions)

    def render(self, guis):
        glBindVertexArray(self.__quad.getVaoID())
        glEnableVertexAttribArray(0)
        for gui in guis:
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.__quad.getVertexCount())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)