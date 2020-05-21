from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix, createProjectionMatrix


class Renderer:
    __FOV = 70
    __NEAR_PLANE = 0.1
    __FAR_PLANE = 1000

    def __init__(self, shader, window):
        self.__width = window.width
        self.__height = window.height
        self.__createProjectionMatrix()
        shader.start()
        shader.loadProjectionMatrix(self.__projectionMatrix)
        shader.stop()

    def prepare(self, time):
        glEnable(GL_DEPTH_TEST)
        self.__applicationTime = time
        glClearColor(0.0, 0.0, 0.0, 0.0)  # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER
        #glFrontFace(GL_CW)

    def render(self, entity, shader):
        texturedModel = entity.getModel()
        model = texturedModel.getRawModel()
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        transformationMatrix = createTransformationMatrix(entity.getPosition(), entity.getRotX(), entity.getRotY(), entity.getRotZ(), entity.getScale(), self.__applicationTime)
        shader.loadTransformationMatrix(transformationMatrix)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturedModel.getTexture().getID())
        glDrawArrays(GL_TRIANGLE_FAN, 0, model.getVertexCount())
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindVertexArray(0)

    def __createProjectionMatrix(self):
        self.__projectionMatrix = createProjectionMatrix(self.__FOV, self.__width, self.__height, self.__NEAR_PLANE, self.__FAR_PLANE)
