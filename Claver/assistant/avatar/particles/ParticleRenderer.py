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

    def __init__(self, loader, projectionMatrix, camera):
        self.__quad = loader.load2DToVAO(self.__VERTICES, 2)
        self.__camera = camera
        self.__shader = ParticleShader()
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, particles_dict):
        viewMatrix = self.__camera.getViewMatrix()
        self.__prepare()
        for texture in particles_dict:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture.getTextureID())
            for particle in particles_dict[texture]:
                self.__updateModelViewMatrix(particle.getPosition(), particle.getRotation(), particle.getScale(), viewMatrix)
                self.__shader.loadTextureCoordInfo(particle.getTexOffset1(), particle.getTexOffset2(), texture.getNumberOfRows(), particle.getBlend())
                glDrawArrays(GL_TRIANGLE_STRIP, 0, self.__quad.getVertexCount())
        self.__finishRendering()

    def cleanUp(self):
        self.__shader.cleanUp()

    def __updateModelViewMatrix(self, position, rotation, scale, viewMatrix):
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
        self.__shader.loadModelViewMatrix(modelViewMatrix)


    def __prepare(self):
        self.__shader.start()
        glBindVertexArray(self.__quad.getVaoID())
        glEnableVertexAttribArray(0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(False)

    def __finishRendering(self):
        glDepthMask(True)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

