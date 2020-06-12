from OpenGL.GL import *
from pyrr import Matrix44, Vector4, Vector3, Quaternion
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
        self.__cube = loader.load2DToVAO(__VERTICES, 3)
        self.__texture = loader.loadCubeMap(__TEXTURE_FILES)
        self.__shader = SkyboxShader()
        self.__shader.start()
        self.__shader.loadProjectionMatrix(projectionMatrix)
        self.__shader.stop()

    def render(self, camera, r, g, b, clock):
        self.__shader.start()
        self.__shader.loadViewMatrix(camera, clock)
        self.__shader.loadFogColour(r, g, b)
        glBindVertexArray(self.__cube.getVaoID())
        glEnableVertexAttribArray(0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.__texture)
        glDrawArrays(GL_TRIANGLES, 0, self.__cube.getVertexCount())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()
