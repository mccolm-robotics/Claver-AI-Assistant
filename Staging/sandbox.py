import os
from dataclasses import dataclass
from pyrr import Vector3

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

class FontType:
    # Creates a new font and loads up the data about each character from the font file.
	#  *
	#  * (int) textureAtlas - the ID of the font atlas texture.
	#  * (TextMeshCreator) fontFile - the font file containing information about each character in
	#  *                   the texture atlas.
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

    def createTextMesh(GUIText
text) {
    List < Line > lines = createStructure(text);
TextMeshData
data = createQuadVertices(text, lines);
return data;
}

private
List < Line > createStructure(GUIText
text) {
char[]
chars = text.getTextString().toCharArray();
List < Line > lines = new
ArrayList < Line > ();
Line
currentLine = new
Line(metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize());
Word
currentWord = new
Word(text.getFontSize());
for (char c: chars) {
    int ascii = (int) c;
if (ascii == SPACE_ASCII) {
boolean added = currentLine.attemptToAddWord(currentWord);
if (!added) {
lines.add(currentLine);
currentLine = new Line(metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize());
currentLine.attemptToAddWord(currentWord);
}
currentWord = new Word(text.getFontSize());
continue;
}
Character
character = metaData.getCharacter(ascii);
currentWord.addCharacter(character);
}
completeStructure(lines, currentLine, currentWord, text);
return lines;
}

private
void
completeStructure(List < Line > lines, Line
currentLine, Word
currentWord, GUIText
text) {
boolean
added = currentLine.attemptToAddWord(currentWord);
if (!added) {
lines.add(currentLine);
currentLine = new Line(metaData.getSpaceWidth(), text.getFontSize(), text.getMaxLineSize());
currentLine.attemptToAddWord(currentWord);
}
lines.add(currentLine);
}

private
TextMeshData
createQuadVertices(GUIText
text, List < Line > lines) {
text.setNumberOfLines(lines.size());
double
curserX = 0
f;
double
curserY = 0
f;
List < Float > vertices = new
ArrayList < Float > ();
List < Float > textureCoords = new
ArrayList < Float > ();
for (Line line: lines) {
if (text.isCentered()) {
curserX = (line.getMaxLength() - line.getLineLength()) / 2;
}
for (Word word: line.getWords()) {
for (Character letter: word.getCharacters()) {
addVerticesForCharacter(curserX, curserY, letter, text.getFontSize(), vertices);
addTexCoords(textureCoords, letter.getxTextureCoord(), letter.getyTextureCoord(),
letter.getXMaxTextureCoord(), letter.getYMaxTextureCoord());
curserX += letter.getxAdvance() * text.getFontSize();
}
curserX += metaData.getSpaceWidth() * text.getFontSize();
}
curserX = 0;
curserY += LINE_HEIGHT * text.getFontSize();
}
return new
TextMeshData(listToArray(vertices), listToArray(textureCoords));
}

private
void
addVerticesForCharacter(double
curserX, double
curserY, Character
character, double
fontSize,
List < Float > vertices) {
double
x = curserX + (character.getxOffset() * fontSize);
double
y = curserY + (character.getyOffset() * fontSize);
double
maxX = x + (character.getSizeX() * fontSize);
double
maxY = y + (character.getSizeY() * fontSize);
double
properX = (2 * x) - 1;
double
properY = (-2 * y) + 1;
double
properMaxX = (2 * maxX) - 1;
double
properMaxY = (-2 * maxY) + 1;
addVertices(vertices, properX, properY, properMaxX, properMaxY);
}

private
static
void
addVertices(List < Float > vertices, double
x, double
y, double
maxX, double
maxY) {
vertices.add((float)
x);
vertices.add((float)
y);
vertices.add((float)
x);
vertices.add((float)
maxY);
vertices.add((float)
maxX);
vertices.add((float)
maxY);
vertices.add((float)
maxX);
vertices.add((float)
maxY);
vertices.add((float)
maxX);
vertices.add((float)
y);
vertices.add((float)
x);
vertices.add((float)
y);
}

private
static
void
addTexCoords(List < Float > texCoords, double
x, double
y, double
maxX, double
maxY) {
texCoords.add((float)
x);
texCoords.add((float)
y);
texCoords.add((float)
x);
texCoords.add((float)
maxY);
texCoords.add((float)
maxX);
texCoords.add((float)
maxY);
texCoords.add((float)
maxX);
texCoords.add((float)
maxY);
texCoords.add((float)
maxX);
texCoords.add((float)
y);
texCoords.add((float)
x);
texCoords.add((float)
y);
}


private
static
float[]
listToArray(List < Float > listOfFloats)
{
float[]
array = new
float[listOfFloats.size()];
for (int i = 0; i < array.length; i++) {
    array[i] = listOfFloats.get(i);
}
return array;
}



font = MetaFile("res/pop.fnt")
