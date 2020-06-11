from pyrr import Vector3


class Light:

    def __init__(self, position, colour, attenuation=Vector3((1, 0, 0))):
        self.__position = position
        self.__colour = colour
        self.__attenuation = attenuation

    def getAttenuation(self):
        return self.__attenuation

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def getColour(self):
        return self.__colour

    def setColour(self, colour):
        self.__colour = colour