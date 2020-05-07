import os
from dataclasses import dataclass


@dataclass
class Character:
    id: int
    xTextureCoord: float
    yTextureCoord: float
    xTexSize: float
    yTexSize: float
    xOffset: float
    yOffset: float
    sizeX: float
    sizeY: float
    xAdvance: float


class MetaFile:
    meta_data = {}
    values_dict = {}
    PAD_TOP = 0
    PAD_LEFT = 1
    PAD_BOTTOM = 2
    PAD_RIGHT = 3
    DESIRED_PADDING = 3
    LINE_HEIGHT = 0.03
    SPACE_ASCII = 32

    def __init__(self, fileName):
        self.aspectRatio = 500 / 300
        self.openFile(fileName)
        self.loadPaddingData()
        self.loadLineSizes()
        imageWidth = self.getValueOfVariable("scaleW")
        self.loadCharacterData(imageWidth)
        self.close()
        #print(self.meta_data)

    def getCharacter(self, ascii):
        return self.char_dict.get(ascii)

    def getValueOfVariable(self, variable):
        value = self.values_dict.get(variable)
        if value is not None:
            return int(self.values_dict.get(variable))

    def getValuesListOfVariable(self, variable):
        # Split the string value by ','
        numbers = self.values_dict.get(variable).split(",")
        # Convert strings to int in list
        numbers = [int(i) for i in numbers]
        return numbers

    def processNextLine(self):
        self.values_dict.clear()
        line = ""
        try:
            line = self.font_file.readline()
        except EOFError as e:
            print(e)
        else:
            if line == "":
                return False
            # Collapse extra spaces into single space
            line = ' '.join(line.split())
            # Split cleaned up string along spaces
            listOfGroups = line.split(" ")
            # For each substring
            for group in listOfGroups:
                # Split the substring by '='
                parts = group.split("=")
                # If the substring breaks into 2 parts
                if len(parts) == 2:
                    # Add these parts to the dictionary
                    self.values_dict[parts[0]] = parts[1]
            return True

    def openFile(self, file):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(THIS_FOLDER, file)
        try:
            self.font_file = open(file)
        except OSError:
            print("Unable to open font file")

    def close(self):
        self.font_file.close()

    def loadPaddingData(self):
        self.processNextLine()
        self.padding = self.getValuesListOfVariable("padding")
        self.paddingWidth = self.padding[self.PAD_LEFT] + self.padding[self.PAD_RIGHT]
        self.paddingHeight = self.padding[self.PAD_TOP] + self.padding[self.PAD_BOTTOM]

    def loadLineSizes(self):
        self.processNextLine()
        lineHeightPixels = self.getValueOfVariable("lineHeight") - self.paddingHeight
        self.verticalPerPixelSize = self.LINE_HEIGHT / lineHeightPixels
        self.horizontalPerPixelSize = self.verticalPerPixelSize / self.aspectRatio

    def loadCharacterData(self, imageWidth):
        self.processNextLine()
        self.processNextLine()
        while self.processNextLine():
            character = self.loadCharacter(imageWidth)
            if character != None:
                self.meta_data[character.id] = character

    def loadCharacter(self, imageSize):
        id = self.getValueOfVariable("id")
        if id == None:
            return None
        if id == self.SPACE_ASCII:
            self.spaceWidth = (self.getValueOfVariable("xadvance") - self.paddingWidth) * self.horizontalPerPixelSize
            return None
        xTex = (self.getValueOfVariable("x") + (self.padding[self.PAD_LEFT] - self.DESIRED_PADDING)) / imageSize
        yTex = (self.getValueOfVariable("y") + (self.padding[self.PAD_TOP] - self.DESIRED_PADDING)) / imageSize
        width = self.getValueOfVariable("width") - (self.paddingWidth - (2 * self.DESIRED_PADDING))
        height = self.getValueOfVariable("height") - ((self.paddingHeight) - (2 * self.DESIRED_PADDING))
        quadWidth = width * self.horizontalPerPixelSize
        quadHeight = height * self.verticalPerPixelSize
        xTexSize = width / imageSize
        yTexSize = height / imageSize
        xOff = (self.getValueOfVariable("xoffset") + self.padding[self.PAD_LEFT] - self.DESIRED_PADDING) * self.horizontalPerPixelSize
        yOff = (self.getValueOfVariable("yoffset") + (self.padding[self.PAD_TOP] - self.DESIRED_PADDING)) * self.verticalPerPixelSize
        xAdvance = (self.getValueOfVariable("xadvance") - self.paddingWidth) * self.horizontalPerPixelSize
        return Character(id, xTex, yTex, xTexSize, yTexSize, xOff, yOff, quadWidth, quadHeight, xAdvance)


class TextMeshData:
    vertexPositions = []
    textureCoords = []

    def TextMeshData(self, vertexPositions, textureCoords):
        self.vertexPositions = vertexPositions
        self.textureCoords = textureCoords

    def getVertexCount(self):
        return len(self.vertexPositions) / 2

class Word:
    width = 0
    characters = []

    def __init__(self, fontSize):
        self.fontSize = fontSize

    # Adds a character to the end of the current word and increases the screen-space width of the word.
    def addCharacter(self, character):
        self.characters.append(character)
        self.width += character.getxAdvance() * self.fontSize

class Line:
    maxLength = 0
    spaceSize = 0
    words = []
    currentLineLength = 0

    def __init__(self, spaceWidth, fontSize, maxLength):
        self.spaceSize = spaceWidth * fontSize
        self.maxLength = maxLength

    # Attempt to add a word to the line. If the line can fit the word in
    # without reaching the maximum line length then the word is added and the
    # line length increased.
    def attemptToAddWord(self, word):
        additionalLength = word.getWordWidth()
        if self.words:
            additionalLength += self.spaceSize
        else:
            additionalLength += 0
            
        if (self.currentLineLength + additionalLength) <= self.maxLength:
            self.words.append(word)
            self.currentLineLength += additionalLength
            return True
        else:
            return False


class TextMeshCreator:
    LINE_HEIGHT = 0.03
    SPACE_ASCII = 32

    def __init__(self, metaFile):
        self.metaData = MetaFile(metaFile)





font = MetaFile("res/pop.fnt")
