import numpy as np

from Claver.assistant.avatar.models.RawModel import *
from OpenGL.GL import *

class Loader:
    def __init__(self):
        self.__vaos = []
        self.__vbos = []

    # * ( [float] ) positions
    def loadToVAO(self, positions):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, positions)
        self.unbindVAO()
        return RawModel(vaoID, len(positions)/3)

    def cleanUp(self):
        for vao in self.__vaos:
            glDeleteVertexArrays(vao)
        for vbo in self.__vbos:
            glDeleteBuffers(vbo)

    def createVAO(self):
        vaoID = GLuint()                                # Holds the name of the vertex array object
        glCreateVertexArrays(1, ctypes.byref(vaoID))    # Creates the vertex array object and initalizes it to default values
        self.__vaos.append(vaoID)
        print(self.__vaos)
        glBindVertexArray(vaoID)                        # Binds the vertex array object to the OpenGL pipeline target
        return vaoID

    def storeDataInAttributeList(self, attribteNumber, data):
        vboID = GLuint()  # Stores the name of the vertex buffer
        self.__vbos.append(vboID)
        glCreateBuffers(1, ctypes.byref(vboID))  # Generates a buffer to hold the vertex data
        vertices = self.storDataInNumpyArray(data)
        glNamedBufferStorage(vboID, vertices.nbytes, vertices, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, vboID)  # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glVertexAttribPointer(attribteNumber, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))  # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def unbindVAO(self):
        glBindVertexArray(0)

    def storDataInNumpyArray(self, data):
        return np.array(data, dtype=np.float32)