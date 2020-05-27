from Claver.assistant.avatar.textures.TerrainTexture import TerrainTexture

class TerrainTexturePack:
    def __init__(self, backgroundTexture, rTexture, gTexture, bTexture):
        self.__backgroundTexture = backgroundTexture
        self.__rTexture = rTexture
        self.__gTexture = gTexture
        self.__bTexture = bTexture

    def getBackgroundTexture(self):
        return self.__backgroundTexture

    def getrTexture(self):
        return self.__rTexture

    def getgTexture(self):
        return self.__gTexture

    def getbTexture(self):
        return self.__bTexture