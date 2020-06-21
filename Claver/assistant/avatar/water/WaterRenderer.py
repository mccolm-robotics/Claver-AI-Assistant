from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.water.WaterTile import WaterTile
from Claver.assistant.avatar.water.WaterShader import WaterShader
from Claver.interface.Settings import res_dir

class WaterRenderer:
    __WAVE_SPEED = 0.03

    def __init__(self, loader, camera, waterFrameBuffers):
        self.__camera = camera
        self.__fbos = waterFrameBuffers
        self.__moveFactor = 0
        self.__dudvTexture = loader.loadTexture(res_dir['HEIGHT_MAPS'] + "waterDUDV.png")
        self.__normalMap = loader.loadTexture(res_dir['HEIGHT_MAPS'] + "normal.png")
        self.__shader = WaterShader()
        self.__shader.start()
        self.__shader.connectTextureUnits()
        projectionMatrix = camera.getProjectionMatrix()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, delta, lakeModel, sun):
        self.prepareRender(delta, lakeModel.getModel(), sun)
        modelMatrix = createTransformationMatrix(lakeModel.getPosition(), 0, 0, 0, WaterTile.TILE_SIZE)
        self.__shader.loadModelMatrix(modelMatrix)
        glDrawArrays(GL_TRIANGLES, 0, lakeModel.getModel().getVertexCount())
        self.unbind()

    def prepareRender(self, delta, model, sun):
        self.__shader.start()
        self.__shader.loadViewMatrix(self.__camera)
        self.__moveFactor += self.__WAVE_SPEED * delta
        self.__moveFactor %= 1
        self.__shader.loadMoveFactor(self.__moveFactor)
        self.__shader.loadLight(sun)
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.getReflectionTexture())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.getRefractionTexture())
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.__dudvTexture)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.__normalMap)
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.getRefractionDepthTexture())

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def unbind(self):
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def cleanUp(self):
        self.__shader.cleanUp()
