class Character:
    def __init__(self, id, xTextureCoord, yTextureCoord, xTexSize, yTexSize, xOffset, yOffset, sizeX, sizeY, xAdvance):
        self.__id = id
        self.__xTextureCoord = xTextureCoord
        self.__yTextureCoord = yTextureCoord
        self.__xOffset = xOffset
        self.__yOffset = yOffset
        self.__sizeX = sizeX
        self.__sizeY = sizeY
        self.__xMaxTextureCoord = xTexSize + xTextureCoord
        self.__yMaxTextureCoord = yTexSize + yTextureCoord
        self.__xAdvance = xAdvance

    def getId(self):
        return self.__id

    def getxTextureCoord(self):
        return self.__xTextureCoord

    def getyTextureCoord(self):
        return self.__yTextureCoord

    def getXMaxTextureCoord(self):
        return self.__xMaxTextureCoord

    def getYMaxTextureCoord(self):
        return self.__yMaxTextureCoord

    def getxOffset(self):
        return self.__xOffset

    def getyOffset(self):
        return self.__yOffset

    def getSizeX(self):
        return self.__sizeX

    def getSizeY(self):
        return self.__sizeY

    def getxAdvance(self):
        return self.__xAdvance