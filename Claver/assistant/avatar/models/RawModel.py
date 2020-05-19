
class RawModel:
    # * ( int ) vaoID
    # * ( int ) vertexCount
    def __init__(self, vaoID, vertexCount):
        self.__vaoID = vaoID
        self.__vertexCount = vertexCount

    def getVaoID(self):
        return self.__vaoID

    def getVertexCount(self):
        return self.__vertexCount