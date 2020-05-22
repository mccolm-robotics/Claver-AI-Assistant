from OpenGL.GL import *

from Claver.assistant.avatar.toolbox.Math import createTransformationMatrix, createProjectionMatrix
from Claver.assistant.avatar.textures.ModelTexture import ModelTexture


class Renderer:
    __FOV = 70
    __NEAR_PLANE = 0.1
    __FAR_PLANE = 1000

    def __init__(self, shader, window):
        self.__width = window.width
        self.__height = window.height
        self.__shader = shader
        self.__createProjectionMatrix()
        shader.start()
        shader.loadProjectionMatrix(self.__projectionMatrix)
        shader.stop()
        glEnable(GL_DEPTH_TEST) # Enable depth testing to ensure pixels closer to the viewer appear closest
        glDepthFunc(GL_LESS)    # Set the type of calculation used by the depth buffer
        glEnable(GL_CULL_FACE)  # Enable face culling
        glCullFace(GL_BACK)     # Discard the back faces of polygons (determined by the vertex winding order)

    def prepare(self, time):
        self.__applicationTime = time
        glClearColor(0.0, 0.0, 0.0, 0.0)  # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER

    def render(self, entitiesDict):
        for texturedModel in entitiesDict:
            self.prepareTexturedModel(texturedModel)
            for entity in entitiesDict[texturedModel]:
                self.prepareInstance(entity)
                glDrawArrays(GL_TRIANGLES, 0, texturedModel.getRawModel().getVertexCount())
            self.unbindTexturedModel()

    def prepareTexturedModel(self, model):
        rawModel = model.getRawModel()
        glBindVertexArray(rawModel.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        texture = model.getTexture()
        self.__shader.loadShineVariables(texture.getShineDamper(), texture.getReflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.getTexture().getID())

    def unbindTexturedModel(self):
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def prepareInstance(self, entity):
        transformationMatrix = createTransformationMatrix(entity.getPosition(), entity.getRotX(), entity.getRotY(),
                                                          entity.getRotZ(), entity.getScale(), self.__applicationTime)
        self.__shader.loadTransformationMatrix(transformationMatrix)

    def __createProjectionMatrix(self):
        self.__projectionMatrix = createProjectionMatrix(self.__FOV, self.__width, self.__height, self.__NEAR_PLANE, self.__FAR_PLANE)

    def updateProjectionMatrix(self, width, height):
        self.__projectionMatrix = createProjectionMatrix(self.__FOV, width, height, self.__NEAR_PLANE, self.__FAR_PLANE)
        self.__shader.start()
        self.__shader.loadProjectionMatrix(self.__projectionMatrix)
        self.__shader.stop()
