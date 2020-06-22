from Claver.assistant.avatar.fontMeshCreator.FontType import FontType
from Claver.assistant.avatar.fontRendering.TextMaster import TextMaster

class GUIText:
    def __init__(self, text, fontSize, font, position, maxLineLength, centered=False):
        self.__textString = text
        self.__fontSize = fontSize
        self.__font = font
        self.__position = position
        self.__lineMaxSize = maxLineLength
        self.__centerText = centered
        self.__colour = [0, 0, 0]
        self.__numberOfLines = 1
        TextMaster.loadText(self)

    def remove(self):
        TextMaster.removeText(self)

    def getFont(self):
        return self.__font

    def setColour(self, r, g, b):
        self.__colour = [r, g, b]

    def getColour(self):
        return self.__colour

    def getNumberOfLines(self):
        return self.__numberOfLines

    def getPosition(self):
        return self.__position

    def getMesh(self):
        return self.__textMeshVao

    def setMeshInfo(self, vao, verticesCount):
        self.__textMeshVao = vao
        self.__vertexCount = verticesCount

    def getVertexCount(self):
        return self.__vertexCount

    def getFontSize(self):
        return self.__fontSize

    def setNumberOfLines(self, number):
        self.__numberOfLines = number

    def isCentered(self):
        return self.__centerText

    def getMaxLineSize(self):
        return self.__lineMaxSize

    def getTextString(self):
        return self.__textString