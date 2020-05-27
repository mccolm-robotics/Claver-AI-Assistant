from OpenGL.GL import *
from pyrr import Matrix44, Vector4, Vector3, Quaternion

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix, createProjectionMatrix
from Claver.assistant.avatar.shaders.TerrainShader import TerrainShader

class TerrainRenderer:
    def __init__(self, shader, projectionMatrix):
        self.__shader = shader
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.connectTextureUnits()
        self.__shader.stop()

    # * ( [Terrain] ) terrains
    def render(self, terrains, clock):
        for terrain in terrains:
            self.prepareTerrain(terrain)
            self.loadModelMatrix(terrain, clock)
            glDrawArrays(GL_TRIANGLES, 0, terrain.getModel().getVertexCount())
            self.unbindTexturedModel()


    def prepareTerrain(self, terrain):
        rawModel = terrain.getModel()
        glBindVertexArray(rawModel.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        self.bindTextures(terrain)
        self.__shader.loadShineVariables(1, 0)

    def bindTextures(self, terrain):
        texturePack = terrain.getTexturePack()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturePack.getBackgroundTexture().getTextureID())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texturePack.getrTexture().getTextureID())
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, texturePack.getgTexture().getTextureID())
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, texturePack.getbTexture().getTextureID())
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, terrain.getBlendMap().getTextureID())

    def unbindTexturedModel(self):
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def loadModelMatrix(self, terrain, clock):
        transformationMatrix = createTransformationMatrix(Vector3((terrain.getX(), 0, terrain.getZ())), 0, 0, 0, 1, clock)
        self.__shader.loadTransformationMatrix(transformationMatrix)