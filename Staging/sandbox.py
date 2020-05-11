import os
from pyrr import Vector3

class Character:

    def __init__(self, id, xTextureCoord, yTextureCoord, xTexSize, yTexSize, xOffset, yOffset, sizeX, sizeY, xAdvance):
        self.id = id
        self.xTextureCoord = xTextureCoord
        self.yTextureCoord = yTextureCoord
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.xMaxTextureCoord = xTexSize + xTextureCoord
        self.yMaxTextureCoord = yTexSize + yTextureCoord
        self.xAdvance = xAdvance

    def __str__(self):
        return 'Character (Id:{}, xTextureCoord:{}, yTextureCoord:{}, xOffset:{}, yOffset:{}, sizeX:{}, sizeY:{}, xMaxTextureCoord:{}, yMaxTextureCoord:{}, xAdvance:{})'.format(self.id, self.xTextureCoord, self.yTextureCoord, self.xOffset, self.yOffset, self.sizeX, self.sizeY, self.xMaxTextureCoord, self.yMaxTextureCoord, self.xAdvance)


class MetaFile:
    meta_data = {}
    values_dict = {}
    PAD_TOP = 0
    PAD_LEFT = 1
    PAD_BOTTOM = 2
    PAD_RIGHT = 3
    DESIRED_PADDING = 3

    def __init__(self, fileName):
        self.aspectRatio = 500 / 300
        self.openFile(fileName)
        self.loadPaddingData()
        self.loadLineSizes()
        imageWidth = self.getValueOfVariable("scaleW")
        self.loadCharacterData(imageWidth)
        self.close()

    def getCharacter(self, ascii):
        return self.meta_data.get(ascii)

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
            print("EXCEPTION: Unable to open font file")

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
        self.verticalPerPixelSize = TextMeshCreator.LINE_HEIGHT / lineHeightPixels
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
        if id == TextMeshCreator.SPACE_ASCII:
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
        self.width += character.xAdvance * self.fontSize

    def __str__(self):
        pass


class Line:
    words = []
    currentLineLength = 0

    def __init__(self, spaceWidth, fontSize, maxLength):
        self.spaceSize = spaceWidth * fontSize
        self.maxLength = maxLength

    # Attempt to add a word to the line. If the line can fit the word in
    # without reaching the maximum line length then the word is added and the
    # line length increased.
    def attemptToAddWord(self, word):
        additionalLength = word.width
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

    def __str__(self):
        pass

class FontType:
    # Creates a new font and loads up the data about each character from the font file.
    #  * (int) textureAtlas - the ID of the font atlas texture.
    #  * (TextMeshCreator) fontFile - the font file containing information about each character in the texture atlas.
    def __init__(self, textureAtlas, fontFile):
        self.textureAtlas = textureAtlas
        self.loader = TextMeshCreator(fontFile)

    # * Takes in an unloaded text and calculates all of the vertices for the quads
    # * on which this text will be rendered. The vertex positions and texture
    # * coords are calculated based on the information from the font file.
    # *
    # * (GUIText) text - the unloaded text.
    # * (TextMeshData) Returns information about the vertices of all the quads.
    def loadText(self, text):
        return self.loader.createTextMesh(text)

class GUIText:
    colour = Vector3([0.0, 0.0, 0.0])

    # Creates a new text, loads the text's quads into a VAO, and adds the text to the screen.
    # *
    # * (String) text - the text.
    # * (float) fontSize - the font size of the text, where a font size of 1 is the default size.
    # * (FontType) font - the font that this text should use.
    # * (Vector2) position - the position on the screen where the top left corner of the
    # *            text should be rendered. The top left corner of the screen is
    # *            (0, 0) and the bottom right is (1, 1).
    # * (float) maxLineLength - basically the width of the virtual page in terms of screen
    # *            width (1 is full screen width, 0.5 is half the width of the
    # *            screen, etc.) Text cannot go off the edge of the page, so if
    # *            the text is longer than this length it will go onto the next
    # *            line. When text is centered it is centered into the middle of
    # *            the line, based on this line length value.
    # * (boolean) centered - whether the text should be centered or not.

    def __init__(self, text, fontSize, font, position, maxLineLength, centered):
        self.textString = text
        self.fontSize = fontSize
        if(isinstance(font, FontType)):
            self.font = font
        else:
            print("ERROR: font must be of type <FontType>")
        self.position = position
        self.lineMaxSize = maxLineLength
        self.centerText = centered
        #TextMaster.loadText(self)

    def remove(self):
        TextMaster.removeText(self)

    def __len__(self):
        return self.lineMaxSize
        # return NotImplemented

    # Set the colour of the text. All values 0 < x < 1
    def setColour(self, r, g, b):
        self.colour = Vector3([r, g, b]) # Just use a tuple? list?

    @property
    def colour(self):
        return self.colour

    @colour.setter
    def colour(self, r, g, b):
        self.colour = Vector3([r, g, b])

    # Returns the ID of the text's VAO, which contains all the vertex data for the quads on which the text will be rendered.
    def getMesh(self):
        return self.textMeshVao

    # Set the VAO and vertex count for this text.
    def setMeshInfo(self, vao, verticesCount):
        self.textMeshVao = vao
        self.vertexCount = verticesCount

    # Sets the number of lines that this text covers (method used only in loading)
    def setNumberOfLines(self, number):
        self.numberOfLines = number


class TextMeshCreator:
    LINE_HEIGHT = 0.03
    SPACE_ASCII = 32

    def __init__(self, metaFile):
        self.metaData = MetaFile(metaFile)

    # (GUIText) text
    def createTextMesh(self, text):
        lines = self.createStructure(text)
        # data = self.createQuadVertices(text, lines)
        # return data

    # (GUIText) text
    def createStructure(self, text):
        chars = text.textString
        lines = []
        currentLine = Line(self.metaData.spaceWidth, text.fontSize, text.lineMaxSize)
        currentWord = Word(text.fontSize)
        for char in chars:
            ascii = ord(char)
            if ascii == self.SPACE_ASCII:
                added = currentLine.attemptToAddWord(currentWord)
                if added is False:
                    print("FALSE")
                    lines.append(currentLine)
                    currentLine = Line(self.metaData.spaceWidth, text.fontSize, text.lineMaxSize)
                    currentLine.attemptToAddWord(currentWord)
                currentWord = Word(text.fontSize)
                continue
            character = self.metaData.getCharacter(ascii)
            currentWord.addCharacter(character)
        self.completeStructure(lines, currentLine, currentWord, text)
        return lines

    # * ([]]) lines - list of lines.
    # * (Line) currentLine
    # * (Word) currentWord
    # * (GUIText) text
    def completeStructure(self, lines, currentLine, currentWord, text):
        added = currentLine.attemptToAddWord(currentWord)
        if added is False:
            lines.append(currentLine)
            currentLine = Line(self.metaData.spaceWidth, text.fontSize, text.lineMaxSize)
            currentLine.attemptToAddWord(currentWord)
        lines.append(currentLine)

    # * ([]]) lines - list of lines.
    # * (GUIText) text
    def createQuadVertices(self, text, lines):
        text.setNumberOfLines(len(lines))
        curserX = 0.0
        curserY = 0.0
        vertices = []
        textureCoords = []
        for line in lines:
            if text.centerText is True:
                curserX = (line.maxLength - line.currentLineLength) / 2

            for word in line.words:
                for letter in word.characters:
                    self.addVerticesForCharacter(curserX, curserY, letter, text.fontSize, vertices)
                    self.addTexCoords(textureCoords, letter.xTextureCoord, letter.yTextureCoord, letter.xMaxTextureCoord, letter.yMaxTextureCoord)
                    curserX += letter.xAdvance() * text.fontSize
                curserX += self.metaData.spaceWidth * text.fontSize
            curserX = 0
            curserY += self.LINE_HEIGHT * text.fontSize
        return TextMeshData(vertices, textureCoords)

    # * (Character) character
    # * ([]) vertices
    def addVerticesForCharacter(self, curserX, curserY, character, fontSize, vertices):
        x = curserX + (character.xOffset * fontSize)
        y = curserY + (character.yOffset * fontSize)
        maxX = x + (character.sizeX * fontSize)
        maxY = y + (character.sizeY * fontSize)
        properX = (2 * x) - 1
        properY = (-2 * y) + 1
        properMaxX = (2 * maxX) - 1
        properMaxY = (-2 * maxY) + 1
        self.addVertices(vertices, properX, properY, properMaxX, properMaxY)

    # * ([]) vertices
    def addVertices(self, vertices, x, y, maxX, maxY):
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
    def addTexCoords(self, texCoords, x, y, maxX, maxY):
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
    def listToArray(self, listOfFloats):
        return [val for val in listOfFloats]


# font = MetaFile("res/pop.fnt")

# Loader loader = new Loader();
# TextMaster.init(loader);
# font = FontType(loader.loadTexture("verdana"), new File("verdana.fnt"));
font = FontType(0, "res/pop.fnt")
# # Parameters (
#     text to render,
#     font size,
#     font,
#     the position,
#     line length -> 1.0 = width of screen,
#     whether text is centered)
my_epic_text = "This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! This is a test text! "
text = GUIText(my_epic_text, 1, font, (0,0), 1.0, True)
data = font.loadText(text)  # (TextMeshData) data
# text.setColour(1,0,0);
