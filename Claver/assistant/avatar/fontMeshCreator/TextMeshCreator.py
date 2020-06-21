from Claver.assistant.avatar.fontMeshCreator.MetaFile import MetaFile
from Claver.assistant.avatar.fontMeshCreator.Word import Word
from Claver.assistant.avatar.fontMeshCreator.Line import Line
from Claver.assistant.avatar.fontMeshCreator.Character import Character
from Claver.assistant.avatar.fontMeshCreator.TextMeshData import TextMeshData
from Claver.assistant.avatar.fontMeshCreator.GUIText import GUIText

class TextMeshCreator:

    LINE_HEIGHT = 0.03
    SPACE_ASCII = 32

    def __init__(self, metaFile, window_rect):
        self.__metaData = MetaFile(metaFile, window_rect)

    # (GUIText) text
    def createTextMesh(self, text):
        lines = self.__createStructure(text)
        data = self.__createQuadVertices(text, lines)
        return data

    # (GUIText) text
    def __createStructure(self, text):
        chars = text.getTextString()
        lines = []
        currentLine = Line(self.__metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize())
        currentWord = Word(text.getFontSize())
        for char in chars:
            ascii = ord(char)
            if ascii == self.SPACE_ASCII:
                added = currentLine.attemptToAddWord(currentWord)
                if added is False:
                    lines.append(currentLine)
                    currentLine = Line(self.__metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize())
                    currentLine.attemptToAddWord(currentWord)
                currentWord = Word(text.getFontSize())
                continue
            character = self.__metaData.getCharacter(ascii)
            currentWord.addCharacter(character)
        self.__completeStructure(lines, currentLine, currentWord, text)
        return lines

    # * ([]]) lines - list of lines.
    # * (Line) currentLine
    # * (Word) currentWord
    # * (GUIText) text
    def __completeStructure(self, lines, currentLine, currentWord, text):
        added = currentLine.attemptToAddWord(currentWord)
        if added is False:
            lines.append(currentLine)
            currentLine = Line(self.__metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize())
            currentLine.attemptToAddWord(currentWord)
        lines.append(currentLine)

    # * ([]]) lines - list of lines.
    # * (GUIText) text
    def __createQuadVertices(self, text, lines):
        text.setNumberOfLines(len(lines))
        curserX = 0.0
        curserY = 0.0
        vertices = []
        textureCoords = []
        for line in lines:
            if text.isCentered() is True:
                curserX = (line.getMaxLength() - line.getLineLength()) / 2

            for word in line.getWords():
                for letter in word.getCharacters():
                    self.__addVerticesForCharacter(curserX, curserY, letter, text.getFontSize(), vertices)
                    self.__addTexCoords(textureCoords, letter.getxTextureCoord(), letter.getyTextureCoord(), letter.getXMaxTextureCoord(), letter.getYMaxTextureCoord())
                    curserX += letter.getxAdvance() * text.getFontSize()
                curserX += self.__metaData.getSpaceWidth() * text.getFontSize()
            curserX = 0
            curserY += self.LINE_HEIGHT * text.getFontSize()
        return TextMeshData(vertices, textureCoords)

    # * (Character) character
    # * ([]) vertices
    def __addVerticesForCharacter(self, curserX, curserY, character, fontSize, vertices):
        x = curserX + (character.getxOffset() * fontSize)
        y = curserY + (character.getyOffset() * fontSize)
        maxX = x + (character.getSizeX() * fontSize)
        maxY = y + (character.getSizeY() * fontSize)
        properX = (2 * x) - 1
        properY = (-2 * y) + 1
        properMaxX = (2 * maxX) - 1
        properMaxY = (-2 * maxY) + 1
        self.__addVertices(vertices, properX, properY, properMaxX, properMaxY)

    # * ([]) vertices
    def __addVertices(self, vertices, x, y, maxX, maxY):
        vertices.append(x)
        vertices.append(y)
        vertices.append(x)
        vertices.append(maxY)
        vertices.append(maxX)
        vertices.append(maxY)
        vertices.append(maxX)
        vertices.append(maxY)
        vertices.append(maxX)
        vertices.append(y)
        vertices.append(x)
        vertices.append(y)

    # * ([]) texCoords
    def __addTexCoords(self, texCoords, x, y, maxX, maxY):
        texCoords.append(x)
        texCoords.append(y)
        texCoords.append(x)
        texCoords.append(maxY)
        texCoords.append(maxX)
        texCoords.append(maxY)
        texCoords.append(maxX)
        texCoords.append(maxY)
        texCoords.append(maxX)
        texCoords.append(y)
        texCoords.append(x)
        texCoords.append(y)

    # * ([]) listOfFloats
    def __listToArray(self, listOfFloats):
        return [val for val in listOfFloats]