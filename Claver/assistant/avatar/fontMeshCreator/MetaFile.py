import os
from Claver.assistant.avatar.fontMeshCreator.Character import Character

class MetaFile:

    __PAD_TOP = 0
    __PAD_LEFT = 1
    __PAD_BOTTOM = 2
    __PAD_RIGHT = 3
    __DESIRED_PADDING = 3

    def __init__(self, fileName, window_rect):
        self.__aspectRatio = window_rect.width / window_rect.height
        self.__metaData_dict = {}
        self.__values_dict = {}
        self.__openFile(fileName)
        self.__loadPaddingData()
        self.__fontName = self.getFontName().strip('"')
        self.__loadLineSizes()
        imageWidth = self.__getValueOfVariable("scaleW")
        self.__loadCharacterData(imageWidth)
        self.__close()

    def getFontName(self):
        return self.__values_dict.get("face")

    def getSpaceWidth(self):
        return self.__spaceWidth

    def getCharacter(self, ascii):
        return self.__metaData_dict.get(ascii)

    def __processNextLine(self):
        self.__values_dict.clear()
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
                    self.__values_dict[parts[0]] = parts[1]
            return True

    def __getValueOfVariable(self, variable):
        value = self.__values_dict.get(variable)
        if value is not None:
            return int(self.__values_dict.get(variable))

    def __getValuesListOfVariable(self, variable):
        # Split the string value by ','
        numbers = self.__values_dict.get(variable).split(",")
        # Convert strings to int in list
        numbers = [int(i) for i in numbers]
        return numbers

    def __close(self):
        self.font_file.close()

    def __openFile(self, file):
        try:
            self.font_file = open(file)
        except OSError:
            print("EXCEPTION: Unable to open font file")

    def __loadPaddingData(self):
        self.__processNextLine()
        self.padding = self.__getValuesListOfVariable("padding")
        self.paddingWidth = self.padding[self.__PAD_LEFT] + self.padding[self.__PAD_RIGHT]
        self.paddingHeight = self.padding[self.__PAD_TOP] + self.padding[self.__PAD_BOTTOM]

    def __loadLineSizes(self):
        from Claver.assistant.avatar.fontMeshCreator.TextMeshCreator import TextMeshCreator
        self.__processNextLine()
        lineHeightPixels = self.__getValueOfVariable("lineHeight") - self.paddingHeight
        self.verticalPerPixelSize = TextMeshCreator.LINE_HEIGHT / lineHeightPixels
        self.horizontalPerPixelSize = self.verticalPerPixelSize / self.__aspectRatio

    def __loadCharacterData(self, imageWidth):
        self.__processNextLine()
        self.__processNextLine()
        while self.__processNextLine():
            character = self.__loadCharacter(imageWidth)
            if character != None:
                self.__metaData_dict[character.getId()] = character

    def __loadCharacter(self, imageSize):
        from Claver.assistant.avatar.fontMeshCreator.TextMeshCreator import TextMeshCreator
        id = self.__getValueOfVariable("id")
        if id == None:
            return None
        if id == TextMeshCreator.SPACE_ASCII:
            self.__spaceWidth = (self.__getValueOfVariable("xadvance") - self.paddingWidth) * self.horizontalPerPixelSize
            return None
        xTex = (self.__getValueOfVariable("x") + (self.padding[self.__PAD_LEFT] - self.__DESIRED_PADDING)) / imageSize
        yTex = (self.__getValueOfVariable("y") + (self.padding[self.__PAD_TOP] - self.__DESIRED_PADDING)) / imageSize
        width = self.__getValueOfVariable("width") - (self.paddingWidth - (2 * self.__DESIRED_PADDING))
        height = self.__getValueOfVariable("height") - ((self.paddingHeight) - (2 * self.__DESIRED_PADDING))
        quadWidth = width * self.horizontalPerPixelSize
        quadHeight = height * self.verticalPerPixelSize
        xTexSize = width / imageSize
        yTexSize = height / imageSize
        xOff = (self.__getValueOfVariable("xoffset") + self.padding[self.__PAD_LEFT] - self.__DESIRED_PADDING) * self.horizontalPerPixelSize
        yOff = (self.__getValueOfVariable("yoffset") + (self.padding[self.__PAD_TOP] - self.__DESIRED_PADDING)) * self.verticalPerPixelSize
        xAdvance = (self.__getValueOfVariable("xadvance") - self.paddingWidth) * self.horizontalPerPixelSize
        return Character(id, xTex, yTex, xTexSize, yTexSize, xOff, yOff, quadWidth, quadHeight, xAdvance)
