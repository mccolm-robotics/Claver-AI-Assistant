class WaterTile:
    TILE_SIZE = 10

    def __init__(self, centerX, height, centerZ):
        self.__x = centerX
        self.__height = height
        self.__z = centerZ

    def getX(self):
        return self.__x

    def getHeight(self):
        return self.__height

    def getZ(self):
        return self.__z

    def __str__(self):
        return "WaterTile (centerX:{} centerZ:{} height:{})".format(self.__x, self.__z, self.__height)