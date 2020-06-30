import numpy as np
import os
from Claver.assistant.avatar.models.RawModel import RawModel
from Claver.assistant.avatar.textures.TextureData import TextureData
from Claver.interface.Settings import res_dir
from OpenGL.GL import *
from PIL import Image

class Loader:
    def __init__(self):
        self.__vaos = np.empty(0, dtype=np.uint32)
        self.__vbos = np.empty(0, dtype=np.uint32)
        self.__textures = np.empty(0, dtype=np.uint32)

    # * ( [float] ) positions
    def loadToVAO(self, positions, textureCoords=None, normals=None, tangents=None):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, 3, positions)
        if textureCoords is not None:
            self.storeDataInAttributeList(1, 3, textureCoords)
        if normals is not None:
            self.storeDataInAttributeList(2, 3, normals)
        if tangents is not None:
            self.storeDataInAttributeList(3, 3, tangents)

        self.unbindVAO()

        return RawModel(vaoID, len(positions))

    def loadQuadToVAO(self, positions, textureCoords):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, 2, positions)
        self.storeDataInAttributeList(1, 2, textureCoords)
        self.unbindVAO()
        return vaoID

    def load2DToVAO(self, positions, dimensions=2):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, dimensions, positions)
        self.unbindVAO()
        return RawModel(vaoID, int(len(positions)/dimensions))

    def storeDataInAttributeList(self, attributeNumber, coordinateSize, data):
        vboID = GLuint()  # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(vboID))  # Generates a buffer to hold the vertex data
        self.__vbos = np.append(self.__vbos, vboID)
        np_data = self.storDataInNumpyArray(data)
        glNamedBufferStorage(vboID, np_data.nbytes, np_data, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, vboID)  # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glVertexAttribPointer(attributeNumber, coordinateSize, GL_FLOAT, GL_FALSE, np_data.itemsize * coordinateSize, ctypes.c_void_p(0))  # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def createEmptyVbo(self, floatCount):
        vboID = GLuint()  # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(vboID))  # Generates a buffer to hold the vertex data
        self.__vbos = np.append(self.__vbos, vboID)
        glNamedBufferData(vboID, floatCount * 4, ctypes.c_void_p(0), GL_STREAM_DRAW)  # Allocates buffer memory and initializes it with vertex data
        return vboID

    def addInstancedAttribute(self, vaoID, vboID, attributeNum, dataSize, instancedDataLength, offset):
        glBindBuffer(GL_ARRAY_BUFFER, vboID)
        glBindVertexArray(vaoID)
        # Add an attribute to the VAO
        glVertexAttribPointer(attributeNum, dataSize, GL_FLOAT, GL_FALSE, instancedDataLength * 4, ctypes.c_void_p(offset * 4))
        # Indicate that this is a per-instance attribute
        glVertexAttribDivisor(attributeNum, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def updateVbo(self, vboID, data):
        np_data = self.storDataInNumpyArray(data)
        glBindBuffer(GL_ARRAY_BUFFER, vboID)
        glBufferData(GL_ARRAY_BUFFER, np_data.nbytes, ctypes.c_void_p(0), GL_STREAM_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, np_data)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def loadTexture(self, fileName, flipped=True):
        textureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureID)

        image = Image.open(fileName)
        if flipped is True:
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = np.array(list(flipped_image.getdata()), np.uint8)
        else:
            img_data = np.array(list(image.getdata()), np.uint8)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        image.close()

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, -0.4)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)
        self.__textures = np.append(self.__textures, textureID)
        return textureID

    def loadCubeMap(self, textureFiles, directory):
        textureID = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, textureID)

        for i in range(len(textureFiles)):
            data = self.decodeTextureFile(directory + "{}.png".format(textureFiles[i]))
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGBA, data.getWidth(), data.getHeight(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data.getBuffer())

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        self.__textures = np.append(self.__textures, textureID)
        return textureID

    def decodeTextureFile(self, fileName, flipped=False):
        image = Image.open(fileName)
        width, height = image.size
        if flipped is True:
            flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = np.array(list(flipped_image.getdata()), np.uint8)
        else:
            img_data = np.array(list(image.getdata()), np.uint8)
        image.close()
        return TextureData(img_data, width, height)

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

    def unbindVAO(self):
        glBindVertexArray(0)

    def storDataInNumpyArray(self, data):
        return np.array(data, dtype=np.float32)