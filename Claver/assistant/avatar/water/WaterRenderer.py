from OpenGL.GL import *
from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.water.WaterTile import WaterTile

class WaterRenderer:
    def __init__(self, loader, shader, projectionMatrix):
        self.__shader = shader
        shader.start()
        shader.loadProjectionMatrix(projectionMatrix)
        shader.stop()
        self.__quad = self.initializeVAO(loader)

    def render(self, waterTile, camera):
        self.prepareRender(camera)
        for tile in waterTile:
            modelMatrix = createTransformationMatrix((tile.getX(), tile.getHeight(), tile.getZ()), 0, 0, 0, WaterTile.TILE_SIZE)
            self.__shader.loadModelMatrix(modelMatrix)
            glDrawArrays(GL_TRIANGLES, 0, self.__quad.getVertexCount())
        self.unbind()

    def prepareRender(self, camera):
        self.__shader.start()
        self.__shader.loadViewMatrix(camera)
        glBindVertexArray(self.__quad.getVaoID())
        glEnableVertexAttribArray(0)

    def unbind(self):
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def initializeVAO(self, loader):
        vertices = [
            -1, 0, -1,
            -1, 0, 1,
            1, 0, -1,
            1, 0, -1,
            -1, 0, 1,
            1, 0, 1
        ]
        return loader.loadToVAO(vertices)
