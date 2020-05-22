class Light:

    def __init__(self, position, colour):
        self.__position = position
        self.__colour = colour

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getColour(self):
        return self.__colour

    def setColour(self, colour):
        self.__colour = colour