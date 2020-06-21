from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.basicShader.BasicTile import BasicTile


class BasicRenderer:

    def __init__(self, shader, projectionMatrix, camera):
        self.__camera = camera
        self.__shader = shader
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, basicModel, clock):
        self.__shader.start()
        self.prepareRender(basicModel.getModel())
        modelMatrix = createTransformationMatrix(basicModel.getPosition(), 0, 0, 0, BasicTile.TILE_SIZE)
        self.__shader.loadModelMatrix(modelMatrix)
        glDrawArrays(GL_TRIANGLES, 0, basicModel.getModel().getVertexCount())
        self.unbind()
        self.__shader.stop()

    def prepareRender(self, model):
        self.__shader.loadViewMatrix(self.__camera)
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)

    def unbind(self):
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)

