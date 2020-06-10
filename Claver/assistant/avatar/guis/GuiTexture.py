class GuiTexture:
    def __init__(self, texture, position, scale):
        self.__texture = texture
        self.__position = position
        self.__scale = scale

    def getTexture(self):
        return self.__texture

    def getPosition(self):
        return self.__position

    def getScale(self):
        return self.__scale