class Light:
    def __init__(self, position, colour, attenuation=(1.0, 0.0, 0.0)):
        self.position = position
        self.colour = colour
        self.attenuation = attenuation

    def getAttenuation(self):
        return self.attenuation

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getColour(self):
        return self.colour

    def setColour(self, colour):
        self.colour = colour
