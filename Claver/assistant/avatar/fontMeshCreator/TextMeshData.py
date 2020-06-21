class TextMeshData:
    def __init__(self, vertexPositions, textureCoords):
        self.__vertexPositions = vertexPositions
        self.__textureCoords = textureCoords

    def getVertexPositions(self):
        return self.__vertexPositions

    def getTextureCoords(self):
        return self.__textureCoords

    def getVertexCount(self):
        return len(self.__vertexPositions) / 2