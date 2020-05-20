import numpy as np

from Claver.assistant.avatar.models.RawModel import *
from OpenGL.GL import *

class Loader:
    def __init__(self):
        self.__vaos = np.empty(0, dtype=np.uint32)
        self.__vbos = np.empty(0, dtype=np.uint32)

    # * ( [float] ) positions
    def loadToVAO(self, positions):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, positions)
        self.unbindVAO()
        return RawModel(vaoID, int(len(positions)/3))

    def cleanUp(self):
        for vao in np.nditer(self.__vaos):
            glDeleteVertexArrays(1, GLuint(vao))
        for vbo in np.nditer(self.__vbos):
            glDeleteBuffers(1, GLuint(vbo))

    def createVAO(self):
        vaoID = GLuint()                                # Holds the name of the vertex array object
        glCreateVertexArrays(1, ctypes.byref(vaoID))    # Creates the vertex array object and initalizes it to default values
        self.__vaos = np.append(self.__vaos, vaoID)
        glBindVertexArray(vaoID)                        # Binds the vertex array object to the OpenGL pipeline target
        return vaoID

    def storeDataInAttributeList(self, attribteNumber, data):
        vboID = GLuint()  # Stores the name of the vertex buffer
        glCreateBuffers(1, ctypes.byref(vboID))  # Generates a buffer to hold the vertex data
        self.__vbos = np.append(self.__vbos, vboID)
        vertices = self.storDataInNumpyArray(data)
        glNamedBufferStorage(vboID, vertices.nbytes, vertices, GL_MAP_READ_BIT)  # Allocates buffer memory and initializes it with vertex data
        glBindBuffer(GL_ARRAY_BUFFER, vboID)  # Binds the buffer object to the OpenGL context and specifies that the buffer holds vertex data
        glVertexAttribPointer(attribteNumber, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))  # Describes the data layout of the vertex buffer used by the 'vertex_position' attribute
        glBindBuffer(GL_ARRAY_BUFFER, vboID)

    def unbindVAO(self):
        glBindVertexArray(0)

    def storDataInNumpyArray(self, data):
        return np.array(data, dtype=np.float32)