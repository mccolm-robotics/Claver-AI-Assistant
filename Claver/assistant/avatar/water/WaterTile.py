import numpy as np
from pyrr import Vector3


class WaterTile:

    TILE_SIZE = 70

    vertices = [
        1.0, 0.0, -1.0,
        -1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
        -1.0, 0.0, -1.0,
        -1.0, 0.0, 1.0,
        1.0, 0.0, -1.0
    ]

    def __init__(self, loader, position):
        # self.__model = loader.loadToVAO(self.vertices)
        self.__model = loader.load2DToVAO(self.vertices, 3)
        self.__position = Vector3(position)
        self.__x = self.__position.x
        self.__z = self.__position.z
        self.__height = self.__position.y


    def getModel(self):
        return self.__model

    def getPosition(self):
        return self.__position

    def getX(self):
        return self.__x

    def getZ(self):
        return self.__z

    def getHeight(self):
        return self.__height