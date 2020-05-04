import os



class TextMeshCreator():

    LINE_HEIGHT = 0.03
    SPACE_ASCII = 32

    metaData = MetaFile()




class MetaFile():
    meta_data = {}
    values_dict = {}
    PAD_TOP = 0
    PAD_LEFT = 1
    PAD_BOTTOM = 2
    PAD_RIGHT = 3
    DESIRED_PADDING = 3

    def __init__(self):
        self.aspectRatio = 500/300
        self.openFile("res/pop.fnt")
        self.loadPaddingData()
        #loadLineSizes()
        #imageWidth = getValueOfVariable("scaleW")
        #loadCharacterData(imageWidth)
        self.print_file()
        self.close()

    def getCharacter(self, ascii):
        return self.char_dict.get(ascii)

    def getValueOfVariable(self, variable):
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
            print(line)
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
            print(self.values_dict)

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
        padding = self.getValuesListOfVariable("padding")
        self.paddingWidth = padding[self.PAD_LEFT] + padding[self.PAD_RIGHT]
        self.paddingHeight = padding[self.PAD_TOP] + padding[self.PAD_BOTTOM]

    def loadLineSizes(self):
        self.processNextLine()
        lineHeightPixels = self.getValueOfVariable("lineHeight") - self.paddingHeight
        #verticalPerPixelSize = TextMeshCreator.LINE_HEIGHT / (double) lineHeightPixels
        #horizontalPerPixelSize = verticalPerPixelSize / self.aspectRatio

    def print_file(self):
        self.processNextLine()



font = MetaFile()
