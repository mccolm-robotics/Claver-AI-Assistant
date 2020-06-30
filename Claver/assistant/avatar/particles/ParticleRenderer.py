from OpenGL.GL import *
from pyrr import Matrix44, matrix44
from math import radians


from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.particles.ParticleShader import ParticleShader
from Claver.assistant.avatar.renderEngine.Loader import Loader
from Claver.assistant.avatar.models.RawModel import RawModel
from Claver.assistant.avatar.particles.Particle import Particle
from Claver.assistant.avatar.particles.ParticleTexture import ParticleTexture


class ParticleRenderer:

    __VERTICES = (-0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5)
    __MAX_INSTANCES = 200
    __INSTANCE_DATA_LENGTH = 21     # 16 (model-view matrix) + 4 (texture information) + 1 (blend factor)

    def __init__(self, loader, projectionMatrix, camera):
        self.__loader = loader
        self.__vboID = loader.createEmptyVbo(self.__INSTANCE_DATA_LENGTH * self.__MAX_INSTANCES)
        self.__quad = loader.load2DToVAO(self.__VERTICES, 2)
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 1, 4, self.__INSTANCE_DATA_LENGTH, 0)   # 3rd param: column 'A' of the model-view matrices
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 2, 4, self.__INSTANCE_DATA_LENGTH, 4)
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 3, 4, self.__INSTANCE_DATA_LENGTH, 8)
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 4, 4, self.__INSTANCE_DATA_LENGTH, 12)
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 5, 4, self.__INSTANCE_DATA_LENGTH, 16)
        loader.addInstancedAttribute(self.__quad.getVaoID(), self.__vboID, 6, 1, self.__INSTANCE_DATA_LENGTH, 20)
        self.__camera = camera
        self.__shader = ParticleShader()
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, particles_dict):
        viewMatrix = self.__camera.getViewMatrix()
        self.__prepare()
        for texture in particles_dict:
            self.__bindTexture(texture)
            particleList = particles_dict[texture]
            vboData = []
            for particle in particleList:
                self.__updateModelViewMatrix(particle.getPosition(), particle.getRotation(), particle.getScale(), viewMatrix, vboData)
                self.__updateTexCoordInfo(particle, vboData)
            self.__loader.updateVbo(self.__vboID, vboData)
            glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, self.__quad.getVertexCount(), len(particleList))
        self.__finishRendering()

    def cleanUp(self):
        self.__shader.cleanUp()

    def __updateTexCoordInfo(self, particle, vboData):
        vboData.append(particle.getTexOffset1()[0])
        vboData.append(particle.getTexOffset1()[1])
        vboData.append(particle.getTexOffset2()[0])
        vboData.append(particle.getTexOffset2()[1])
        vboData.append(particle.getBlend())

    def __bindTexture(self, texture):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture.getTextureID())
        self.__shader.loadNumberOfRows(texture.getNumberOfRows())

    def __updateModelViewMatrix(self, position, rotation, scale, viewMatrix, vboData):
        translation = Matrix44.from_translation(position)
        translation.m11 = viewMatrix.m11
        translation.m12 = viewMatrix.m21
        translation.m13 = viewMatrix.m31
        translation.m21 = viewMatrix.m12
        translation.m22 = viewMatrix.m22
        translation.m23 = viewMatrix.m32
        translation.m31 = viewMatrix.m13
        translation.m32 = viewMatrix.m23
        translation.m33 = viewMatrix.m33
        rotation = matrix44.create_from_axis_rotation((0.0, 0.0, 1.0), radians(rotation))
        scale = Matrix44.from_scale([scale, scale, scale])
        modelMatrix = translation * rotation * scale
        modelViewMatrix = viewMatrix * modelMatrix
        self.__storeMatrixData(modelViewMatrix, vboData)

    def __storeMatrixData(self, matrix, vboData):
        vboData.append(matrix.m11)
        vboData.append(matrix.m12)
        vboData.append(matrix.m13)
        vboData.append(matrix.m14)
        vboData.append(matrix.m21)
        vboData.append(matrix.m22)
        vboData.append(matrix.m23)
        vboData.append(matrix.m24)
        vboData.append(matrix.m31)
        vboData.append(matrix.m32)
        vboData.append(matrix.m33)
        vboData.append(matrix.m34)
        vboData.append(matrix.m41)
        vboData.append(matrix.m42)
        vboData.append(matrix.m43)
        vboData.append(matrix.m44)


    def __prepare(self):
        self.__shader.start()
        glBindVertexArray(self.__quad.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glEnableVertexAttribArray(4)
        glEnableVertexAttribArray(5)
        glEnableVertexAttribArray(6)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(False)

    def __finishRendering(self):
        glDepthMask(True)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glDisableVertexAttribArray(4)
        glDisableVertexAttribArray(5)
        glDisableVertexAttribArray(6)
        glBindVertexArray(0)
        self.__shader.stop()

