from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.water.WaterTile import WaterTile
from Claver.assistant.avatar.water.WaterShader import WaterShader


class WaterRenderer:

    def __init__(self, camera, waterFrameBuffers):
        self.__camera = camera
        self.__fbos = waterFrameBuffers
        self.__shader = WaterShader()
        self.__shader.start()
        self.__shader.connectTextureUnits()
        projectionMatrix = camera.getProjectionMatrix()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, lakeModel, clock):
        self.prepareRender(lakeModel.getModel())
        modelMatrix = createTransformationMatrix(lakeModel.getPosition(), 0, 0, 0, WaterTile.TILE_SIZE)
        self.__shader.loadModelMatrix(modelMatrix)
        glDrawArrays(GL_TRIANGLES, 0, lakeModel.getModel().getVertexCount())
        self.unbind()

    def prepareRender(self, model):
        self.__shader.start()
        self.__shader.loadViewMatrix(self.__camera)
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.getReflectionTexture())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.getRefractionTexture())

    def unbind(self):
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def cleanUp(self):
        self.__shader.cleanUp()
