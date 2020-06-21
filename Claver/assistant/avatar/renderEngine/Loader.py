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
        # Creates a buffer to hold the vertex data and binds it to the OpenGL pipeline
        # self.model = np.concatenate((positions, textureCoords), axis=0)
        #
        # self.vertex_buffer_object = GLuint()  # Stores the name of the vertex buffer
        # glCreateBuffers(1, ctypes.byref(self.vertex_buffer_object))  # Generates a buffer to hold the vertex data
        # self.__vbos = np.append(self.__vbos, self.vertex_buffer_object)
        # glNamedBufferStorage(self.vertex_buffer_object, self.model.nbytes, self.model, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        # glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_object)  # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        # self.vertex_position_attribute = glGetAttribLocation(self.shader, 'vertex_position')
        # glEnableVertexAttribArray(self.vertex_position_attribute)
        # # self.model.itemsize*3 specifies the stride (how to step through the data in the buffer). This is important for telling OpenGL how to step through a buffer having concatinated vertex and color data (see: https://youtu.be/bmCYgoCAyMQ).
        # glVertexAttribPointer(self.vertex_position_attribute, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3,
        #                       ctypes.c_void_p(0))
        #
        # self.texture_in = glGetAttribLocation(self.shader, 'texture_position')
        # self.texture_offset = self.model.itemsize * (len(self.model) // 2) * 3
        # # Describe the position data layout in the buffer
        # glVertexAttribPointer(self.texture_in, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3,
        #                       ctypes.c_void_p(self.texture_offset))
        # glEnableVertexAttribArray(self.texture_in)
        self.unbindVAO()
        # length = len(positions) // 3
        # if textureCoords is not None:
        #     length += len(textureCoords) // 3
        # if normals is not None:
        #     length += len(normals) // 3
        # if tangents is not None:
        #     length += len(tangents) // 3
        return RawModel(vaoID, len(positions))

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