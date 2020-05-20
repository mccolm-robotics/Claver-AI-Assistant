import numpy as np
import os
from Claver.assistant.avatar.models.RawModel import *
from OpenGL.GL import *
from PIL import Image

class Loader:
    def __init__(self):
        self.__vaos = np.empty(0, dtype=np.uint32)
        self.__vbos = np.empty(0, dtype=np.uint32)
        self.__textures = np.empty(0, dtype=np.uint32)

    # * ( [float] ) positions
    def loadToVAO(self, positions, textureCoords):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, 3, positions)
        self.storeDataInAttributeList(1, 2, textureCoords)
        self.unbindVAO()
        return RawModel(vaoID, int(len(positions)/3))

    def loadTexture(self, fileName):
        textureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureID)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = Image.open(fileName)
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(flipped_image.getdata()), np.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        image.close()

        glBindTexture(GL_TEXTURE_2D, 0)
        self.__textures = np.append(self.__textures, textureID)
        return textureID

    def cleanUp(self):
        if self.__vaos.size != 0:
            for vao in np.nditer(self.__vaos):
                glDeleteVertexArrays(1, GLuint(vao))
        if self.__vbos.size != 0:
            for vbo in np.nditer(self.__vbos):
                glDeleteBuffers(1, GLuint(vbo))
        if self.__textures.size != 0:
            for texture in np.nditer(self.__textures):
                glDeleteTextures(texture)

    def createVAO(self):
        vaoID = GLuint()                                # Holds the name of the vertex array object
        glCreateVertexArrays(1, ctypes.byref(vaoID))    # Creates the vertex array object and initalizes it to default values
        self.__vaos = np.append(self.__vaos, vaoID)
        glBindVertexArray(vaoID)                        # Binds the vertex array object to the OpenGL pipeline target
        return vaoID

    def storeDataInAttributeList(self, attribteNumber, coordinateSize, data):
        vboID = GLuint()  # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(vboID))  # Generates a buffer to hold the vertex data
        self.__vbos = np.append(self.__vbos, vboID)
        vertices = self.storDataInNumpyArray(data)
        glNamedBufferStorage(vboID, vertices.nbytes, vertices, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, vboID)  # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glVertexAttribPointer(attribteNumber, coordinateSize, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))  # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        glBindBuffer(GL_ARRAY_BUFFER, vboID)

    def unbindVAO(self):
        glBindVertexArray(0)

    def storDataInNumpyArray(self, data):
        return np.array(data, dtype=np.float32)