from OpenGL.GL import *

from Claver.assistant.avatar.normalMappingRenderer.NMShader import NMShader


class NMRenderer:

    def __init__(self, projectionMatrix, camera):
        self.__shader = NMShader(camera)
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.connectTextureUnits()
        self.__shader.stop()

    def render(self, clock, entitiesDict, clipPlane, lights):
        self.__shader.start()
        self.__prepare(clipPlane, lights)
        for texturedModel in entitiesDict:
            self.__prepareTexturedModel(texturedModel)
            for entity in entitiesDict[texturedModel]:
                self.__prepareInstance(entity, clock)
                glDrawArrays(GL_TRIANGLES, 0, texturedModel.getRawModel().getVertexCount())
            self.__unbindTexturedModel()
        self.__shader.stop()

    def cleanUp(self):
        self.__shader.cleanUp()

    def __prepareTexturedModel(self, model):
        from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
        rawModel = model.getRawModel()
        glBindVertexArray(rawModel.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        texture = model.getTexture()
        self.__shader.loadNumberOfRows(texture.getNumberOfRows())
        if texture.isHasTransparency():
            MasterRenderer.disableCulling()
        self.__shader.loadShineVariables(texture.getShineDamper(), texture.getReflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.getTexture().getID())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, model.getTexture().getNormalMap())

    def __unbindTexturedModel(self):
        from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
        MasterRenderer.enableCulling()
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glBindVertexArray(0)

    def __prepareInstance(self, entity, clock):
        self.__shader.loadTransformationMatrix(entity.getTransformationMatrix())
        self.__shader.loadOffset(entity.getTextureXOffset(), entity.getTextureYOffset())

    def __prepare(self, clipPlane, lights):
        from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
        self.__shader.loadClipPlane(clipPlane)
        self.__shader.loadSkyColour(MasterRenderer.RED, MasterRenderer.GREEN, MasterRenderer.BLUE)

        self.__shader.loadLights(lights)
        self.__shader.loadViewMatrix()
