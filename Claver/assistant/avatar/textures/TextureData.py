class TextureData:
    def __init__(self, data, width, height):
        self.__data = data
        self.__width = width
        self.__height = height

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getBuffer(self):
        return self.__data