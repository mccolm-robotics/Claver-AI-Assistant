import numpy as np
import pyrr
from OpenGL.GL import *
from math import radians
from pyrr import Matrix44, Vector4, Vector3, Quaternion
from Claver.interface.Settings import res_dir
from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix
from Claver.assistant.avatar.skybox.SkyboxShader import SkyboxShader

class SkyboxRenderer:
    def __init__(self, loader, projectionMatrix):
        __SIZE = 100
        __VERTICES = [
            -__SIZE, __SIZE, -__SIZE,
            -__SIZE, -__SIZE, -__SIZE,
            __SIZE, -__SIZE, -__SIZE,
            __SIZE, -__SIZE, -__SIZE,
            __SIZE, __SIZE, -__SIZE,
            -__SIZE, __SIZE, -__SIZE,

            -__SIZE, -__SIZE, __SIZE,
            -__SIZE, -__SIZE, -__SIZE,
            -__SIZE, __SIZE, -__SIZE,
            -__SIZE, __SIZE, -__SIZE,
            -__SIZE, __SIZE, __SIZE,
            -__SIZE, -__SIZE, __SIZE,

            __SIZE, -__SIZE, -__SIZE,
            __SIZE, -__SIZE, __SIZE,
            __SIZE, __SIZE, __SIZE,
            __SIZE, __SIZE, __SIZE,
            __SIZE, __SIZE, -__SIZE,
            __SIZE, -__SIZE, -__SIZE,

            -__SIZE, -__SIZE, __SIZE,
            -__SIZE, __SIZE, __SIZE,
            __SIZE, __SIZE, __SIZE,
            __SIZE, __SIZE, __SIZE,
            __SIZE, -__SIZE, __SIZE,
            -__SIZE, -__SIZE, __SIZE,

            -__SIZE, __SIZE, -__SIZE,
            __SIZE, __SIZE, -__SIZE,
            __SIZE, __SIZE, __SIZE,
            __SIZE, __SIZE, __SIZE,
            -__SIZE, __SIZE, __SIZE,
            -__SIZE, __SIZE, -__SIZE,

            -__SIZE, -__SIZE, -__SIZE,
            -__SIZE, -__SIZE, __SIZE,
            __SIZE, -__SIZE, -__SIZE,
            __SIZE, -__SIZE, -__SIZE,
            -__SIZE, -__SIZE, __SIZE,
            __SIZE, -__SIZE, __SIZE
        ]
        __TEXTURE_FILES = [
            "right",
            "left",
            "top",
            "bottom",
            "back",
            "front"
        ]
        __NIGHT_TEXTURE_FILES = [
            "nightRight",
            "nightLeft",
            "nightTop",
            "nightBottom",
            "nightBack",
            "nightFront"
        ]
        self.__time = 0
        self.__cube = loader.load2DToVAO(__VERTICES, 3)
        self.__texture = loader.loadCubeMap(__TEXTURE_FILES, res_dir['SKYBOX_CLOUDS'])
        self.__nightTexture = loader.loadCubeMap(__NIGHT_TEXTURE_FILES, res_dir['SKYBOX_NIGHT'])
        self.__shader = SkyboxShader()
        self.__shader.start()
        self.__shader.connectTextureUnits()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, camera, r, g, b, clock):
        self.__shader.start()
        self.__shader.loadViewMatrix(camera, clock)
        self.loadModelMatrix(camera, clock)
        self.__shader.loadFogColour(r, g, b)
        glBindVertexArray(self.__cube.getVaoID())
        glEnableVertexAttribArray(0)
        self.bindTextures(clock)
        glDrawArrays(GL_TRIANGLES, 0, self.__cube.getVertexCount())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def loadModelMatrix(self, camera, clock):
        transformationMatrix = createTransformationMatrix((0,0,0), 0, .003*clock, 0, 1)
        self.__shader.loadTransformationMatrix(transformationMatrix)

    # def bindTextures(self):
    #     glActiveTexture(GL_TEXTURE0)
    #     glBindTexture(GL_TEXTURE_CUBE_MAP, self.__texture)
    #     glActiveTexture(GL_TEXTURE1)
    #     glBindTexture(GL_TEXTURE_CUBE_MAP, self.__nightTexture)
    #     self.__shader.loadBlendFactor(0.5)

    def bindTextures(self, clock):
        factor = 2
        time = clock % (24 * factor)
        if 0* factor < time < 5* factor:
            texture1 = self.__nightTexture
            texture2 = self.__nightTexture
            blendFactor = (time - 0) / (5 * factor - 0)
        elif 5 * factor < time < 8 * factor:
            texture1 = self.__nightTexture
            texture2 = self.__texture
            blendFactor = (time - 5 * factor) / (8 * factor - 5 * factor)
        elif 8 * factor < time < 21 * factor:
            texture1 = self.__texture
            texture2 = self.__texture
            blendFactor = (time - 8 * factor) / (20 * factor - 8 * factor)
        else:
            texture1 = self.__texture
            texture2 = self.__nightTexture
            blendFactor = (time - 20 * factor) / (24 * factor - 20 * factor)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture2)
        self.__shader.loadBlendFactor(blendFactor)