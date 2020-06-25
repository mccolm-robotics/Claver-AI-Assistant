class ParticleTexture:
    def __init__(self, textureID, numberOfRows):
        self.__textureID = textureID
        self.__numberOfRows = numberOfRows

    def getTextureID(self):
        return self.__textureID

    def getNumberOfRows(self):
        return self.__numberOfRows
