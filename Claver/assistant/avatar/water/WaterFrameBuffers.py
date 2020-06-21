import numpy as np
from OpenGL.GL import *


class WaterFrameBuffers:
    __REFLECTION_WIDTH = 320
    __REFLECTION_HEIGHT = 180

    __REFRACTION_WIDTH = 1280
    __REFRACTION_HEIGHT = 720

    def __init__(self, window_size):
        # Call during game initialization
        self.__window_rect = window_size

    def initializeFramebuffer(self, default_FBO, window_size):
        self.default_FBO = default_FBO
        self.__window_rect = window_size
        self.__REFRACTION_WIDTH = window_size[0]
        self.__REFRACTION_HEIGHT = window_size[1]
        self.__initializeReflectionFrameBuffer()
        self.__initializeRefractionFrameBuffer()


    def cleanUp(self):
        # Call when closing game
        glDeleteFramebuffers(1, self.__reflectionFrameBuffer)
        glDeleteTextures(self.__reflectionTexture)
        glDeleteRenderbuffers(1, self.__reflectionDepthBuffer)
        glDeleteFramebuffers(1, self.__refractionFrameBuffer)
        glDeleteTextures(self.__refractionTexture)
        glDeleteTextures(self.__refractionDepthTexture)

    def bindReflectionFrameBuffer(self):
        # Call before rendering to this FBO
        self.__bindFrameBuffer(self.__reflectionFrameBuffer, self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)

    def bindRefractionFrameBuffer(self):
        # Call before rendering to this FBO
        self.__bindFrameBuffer(self.__refractionFrameBuffer, self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)

    def unbindCurrentFrameBuffer(self):
        # Call to switch to default frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.default_FBO)
        glViewport(0, 0, self.__window_rect[0], self.__window_rect[1])

    def getReflectionTexture(self):
        # Get the resulting texture
        return self.__reflectionTexture

    def getRefractionTexture(self):
        # Get the resulting texture
        return self.__refractionTexture

    def getRefractionDepthTexture(self):
        # Get the resulting depth texture
        return self.__refractionDepthTexture

    def __initializeReflectionFrameBuffer(self):
        self.__reflectionFrameBuffer = self.__createFrameBuffer()
        self.__reflectionTexture = self.__createTextureAttachment(self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)
        self.__reflectionDepthBuffer = self.__createDepthBufferAttachment(self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)
        self.unbindCurrentFrameBuffer()

    def __initializeRefractionFrameBuffer(self):
        self.__refractionFrameBuffer = self.__createFrameBuffer()
        self.__refractionTexture = self.__createTextureAttachment(self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)
        self.__refractionDepthTexture = self.__createDepthTextureAttachment(self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)
        self.unbindCurrentFrameBuffer()

    def __bindFrameBuffer(self, frameBuffer, width, height):
        glBindTexture(GL_TEXTURE_2D, 0)     # Call to make sure the texture isn't bound
        glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)
        glViewport(0, 0, width, height)

    def __createFrameBuffer(self):
        frameBuffer = glGenFramebuffers(1)
        # Generate name for frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)
        # Create the framebuffer
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        # Indicate that we will always render to colour attachment 0
        return frameBuffer

    def __createTextureAttachment(self, width, height):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, texture, 0)
        return texture

    def __createDepthTextureAttachment(self, width, height):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT32, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, texture, 0)
        return texture

    def __createDepthBufferAttachment(self, width, height):
        depthBuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depthBuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthBuffer)
        return depthBuffer