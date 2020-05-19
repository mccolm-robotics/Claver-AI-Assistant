from PIL import Image
import models.ModelData

class Loader:
    def __init__(self):
        # Keep track of all vaos and vbos created so they can be deleted
        self.vaos = []
        self.vbos = []
        self.textures = []

    # Function description:
    #  * (LIST[]) positions, textureCoordinates, normals
    def loadToVAO(self, positions, textureCoordinates, normals):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, 3, positions)
        self.storeDataInAttributeList(1, 2, textureCoordinates)
        self.storeDataInAttributeList(2, 3, normals)
        self.unbindVAO()
        return ModelData(vaoID, positions.length/3)

    def loadGUIToVAO(self, positions, dimensions):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, dimensions, positions)
        self.unbindVAO()
        return ModdelData(vaoID, positions/dimensions)

    # * ( [float] ) positions
    # * ( [float] ) textureCoords
    def loadTextToVAO(self, positions, textureCoords):
        vaoID = self.createVAO()
        self.storeDataInAttributeList(0, 2, positions)
        self.storeDataInAttributeList(1, 2, textureCoords)
        self.unbindVAO()
        return vaoID

    def loadTexture(self, fileName):
        image = Image.open(fileName)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTextParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, -0.4)
        self.textures.append(image)
        return image

    def cleanUp(self):
        for vaoID in self.vaos:
            glDeleteVertexArrays(vaoID)
        for vboID in self.vbos:
            glDeleteBuffers(vboID)
        for texture in self.textures:
            glDeleteTextures(texture)
        self.vaos.clear()
        self.vbos.clear()
        self.textures.clear()

    # Function description:
    def createVAO(self):
        vaoID = glGenVertexArrays()
        self.vaos.append(vaoID)
        glBindVertexArray(vaoID)
        return vaoID

    # Function description:
    #  * (int) attributeNumber
    #  * (LIST[]) data
    def storeDataInAttributeList(self, attributeNumber, coordinateSize, data):
        vboID = glGenBuffers()
        self.vbos.append(vboID)
        glBindBuffer(GL_ARRAY_BUFFER, vboID)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        glVertexAttribPointer(attributeNumber, coordinateSize, GL_FLOAT, false, 0, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)    # Unbind the VBO

    def unbindVAO(self):
        glBindVertexArray(0)
