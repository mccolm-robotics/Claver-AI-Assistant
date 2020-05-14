from PIL import Image
import ModelData

class Loader:
    def __init__(self):
        # Keep track of all vaos and vbos created so they can be deleted
        self.vaos = []
        self.vbos = []
        self.textures = []

    # Function description:
    #  * (LIST[]) positions
    def loadToVAO(self, positions):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, positions)
        self.unbindVAO()
        return ModelData(vaoID, positions.length/3)

    def loadTexture(self, fileName):
        image = Image.open(fileName)
        self.textures.append(image)
        return image

    def cleanUp(self):
        for vaoID in self.vaos:
            glDeleteVertexArrays(vaoID)
        for vboID in self.vbos:
            glDeleteBuffers(vboID)
        self.vaos.clear()
        self.vbos.clear()

    # Function description:
    def createVAO(self):
        vaoID = glGenVertexArrays()
        self.vaos.append(vaoID)
        glBindVertexArray(vaoID)
        return vaoID

    # Function description:
    #  * (int) attributeNumber
    #  * (LIST[]) data
    def storeDataInAttributeList(self, attributeNumber, data):
        vboID = glGenBuffers()
        self.vbos.append(vboID)
        glBindBuffer(GL_ARRAY_BUFFER, vboID)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(attributeNumber, 3, GL_FLOAT, false, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)    # Unbind the VBO

    def unbindVAO(self):
        glBindVertexArray(0)
