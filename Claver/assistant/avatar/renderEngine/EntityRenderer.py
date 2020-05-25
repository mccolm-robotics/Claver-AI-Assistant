from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix, createProjectionMatrix
from Claver.assistant.avatar.textures.ModelTexture import ModelTexture


class EntityRenderer:

    def __init__(self, shader, projectionMatrix):
        self.__shader = shader
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, entitiesDict, clock):
        for texturedModel in entitiesDict:
            self.prepareTexturedModel(texturedModel)
            for entity in entitiesDict[texturedModel]:
                self.prepareInstance(entity, clock)
                glDrawArrays(GL_TRIANGLES, 0, texturedModel.getRawModel().getVertexCount())
            self.unbindTexturedModel()

    def prepareTexturedModel(self, model):
        from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
        rawModel = model.getRawModel()
        glBindVertexArray(rawModel.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        texture = model.getTexture()
        if texture.isHasTransparency():
            MasterRenderer.disableCulling()
        self.__shader.loadFakeLightingVariable(texture.isUseFakeLighting())
        self.__shader.loadShineVariables(texture.getShineDamper(), texture.getReflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.getTexture().getID())

    def unbindTexturedModel(self):
        from Claver.assistant.avatar.renderEngine.MasterRenderer import MasterRenderer
        MasterRenderer.enableCulling()
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def prepareInstance(self, entity, clock):
        transformationMatrix = createTransformationMatrix(entity.getPosition(), entity.getRotX(), entity.getRotY(),
                                                          entity.getRotZ(), entity.getScale(), clock)
        self.__shader.loadTransformationMatrix(transformationMatrix)


