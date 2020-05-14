class Loader:
    def __init__(self):

    # Function description:
    #  * (LIST[]) positions
    def loadToVAO(self, positions):
        vaoID = createVAO()
        storeDataInAttributeList(0, positions)
        unbindVAO()
        return ModelData(vaoID, positions.length/3)

    # Function description:
    def createVAO(self):
        vaoID = glGenVertexArrays()
        glBindVertexArray(vaoID)
        return vaoID

    # Function description:
    #  * (int) attributeNumber
    #  * (LIST[]) data
    def storeDataInAttributeList(self, attributeNumber, data):
        int vboID = glGenBuffers()
        glBindBuffer(GL_ARRAY_BUFFER, vboID)

    def unbindVAO(self):
        glBindVertexArray(0)

    # Function description:
    #  * (LIST[]) data
    def storeDataInFloatBuffer(self, data):
        buffer = []