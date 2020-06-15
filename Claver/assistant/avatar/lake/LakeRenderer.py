from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.lake.LakeTile import LakeTile


class LakeRenderer:

    def __init__(self, shader, projectionMatrix, camera):
        self.__camera = camera
        self.__shader = shader
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, lakeModel, clock):
        self.prepareRender(lakeModel.getModel())
        modelMatrix = createTransformationMatrix(lakeModel.getPosition(), 0, 0, 0, LakeTile.TILE_SIZE)
        self.__shader.loadModelMatrix(modelMatrix)
        glDrawArrays(GL_TRIANGLES, 0, lakeModel.getModel().getVertexCount())
        self.unbind()

    def prepareRender(self, model):
        self.__shader.start()
        self.__shader.loadViewMatrix(self.__camera)
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)

    def unbind(self):
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()
