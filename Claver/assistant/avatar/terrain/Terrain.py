import numpy as np
import pyrr
from math import floor
from pyrr import Vector3
from PIL import Image
from Claver.assistant.avatar.toolbox.Math import barryCentric


class Terrain:
    __SIZE = 80  # How many unit lengths long?
    # __VERTEX_COUNT = 128      # How many sections to break the terrain into
    __MAX_HEIGHT = 5
    __MAX_PIXEL_COLOUR = 256 + 256 + 256

    def __init__(self, gridX, gridZ, loader, texturePack, blendMap, heightMap, id):
        self.__texturePack = texturePack
        self.__blendMap = blendMap
        self.__x = gridX * self.__SIZE
        self.__z = gridZ * self.__SIZE
        self.__model = self.generateTerrain(loader, heightMap)
        self.__VERTEX_COUNT = None
        self.__id = id

    def getX(self):
        return self.__x

    def getZ(self):
        return self.__z

    def getModel(self):
        return self.__model

    def getTexturePack(self):
        return self.__texturePack

    def getBlendMap(self):
        return self.__blendMap

    def getID(self):
        return 'ID: [{}][{}]'.format(self.__id[0], self.__id[1])

    def generateTerrain(self, loader, heightMap):

        image = Image.open(heightMap)
        rgb_image = image.convert('RGB')
        VERTEX_COUNT = image.height
        image.close()

        self.heights = np.empty(shape=[VERTEX_COUNT, VERTEX_COUNT])

        vertices = []
        normals = []
        textureCoords = []
        for i in range(VERTEX_COUNT):
            for j in range(VERTEX_COUNT):
                height = self.__getHeight(j, i, rgb_image)
                self.heights[j][i] = height
                vertices.append(Vector3([j / (VERTEX_COUNT - 1) * self.__SIZE, height, i / (VERTEX_COUNT - 1) * self.__SIZE]))
                normal = self.__calculateNormal(j, i, rgb_image)
                normals.append(normal)
                textureCoords.append(Vector3([j / (VERTEX_COUNT - 1), i / (VERTEX_COUNT - 1), 0.0]))

        # print("generating terrain. size: ", self.__heights[0].size)


        indices = []
        for gz in range(VERTEX_COUNT - 1):
            for gx in range(VERTEX_COUNT - 1):
                topLeft = (gz * VERTEX_COUNT) + gx
                topRight = topLeft + 1
                bottomLeft = ((gz + 1) * VERTEX_COUNT) + gx
                bottomRight = bottomLeft + 1
                indices.append(topLeft)
                indices.append(bottomLeft)
                indices.append(topRight)
                indices.append(topRight)
                indices.append(bottomLeft)
                indices.append(bottomRight)

        finalVertexList = []
        finalNormalList = []
        finalTextCoordsList = []
        for num in range(len(indices)):
            vertexNumber = indices[num]
            finalVertexList.append(Vector3(vertices[vertexNumber]))
            finalNormalList.append(Vector3(normals[vertexNumber]))
            finalTextCoordsList.append(Vector3(textureCoords[vertexNumber]))
        finalVertexList = np.array(finalVertexList)
        finalNormalList = np.array(finalNormalList)
        finalTextCoordsList = np.array(finalTextCoordsList)
        return loader.loadToVAO(finalVertexList, finalTextCoordsList, finalNormalList)

    def getHeightOfTerrain(self, worldX, worldZ):
        terrainX = worldX - self.__x
        terrainZ = worldZ - self.__z
        gridSquareSize = self.__SIZE / (self.heights[0].size - 1)
        gridX = floor(terrainX / gridSquareSize)
        gridZ = floor(terrainZ / gridSquareSize)
        if gridX >= self.heights[0].size - 1 or gridZ >= self.heights[0].size - 1 or gridX < 0 or gridZ < 0:
            return 0
        xCoord = (terrainX % gridSquareSize) / gridSquareSize
        zCoord = (terrainZ % gridSquareSize) / gridSquareSize
        if xCoord <= (1-zCoord):
            answer = barryCentric(Vector3((0, self.heights[gridX][gridZ], 0)), Vector3((1, self.heights[gridX + 1][gridZ], 0)), Vector3((0, self.heights[gridX][gridZ + 1], 1)), (xCoord, zCoord))
        else:
            answer = barryCentric(Vector3((1, self.heights[gridX + 1][gridZ], 0)), Vector3((1, self.heights[gridX + 1][gridZ + 1], 1)), Vector3((0, self.heights[gridX][gridZ + 1], 1)), (xCoord, zCoord))
        return answer

    def __calculateNormal(self, x, z, rgb_image):
        heightL = self.__getHeight(x - 1, z, rgb_image)
        heightR = self.__getHeight(x + 1, z, rgb_image)
        heightD = self.__getHeight(x, z - 1, rgb_image)
        heightU = self.__getHeight(x, z + 1, rgb_image)
        normal = Vector3(pyrr.vector3.normalize((heightL - heightR, 2, heightD - heightU)))
        return normal

    def __getHeight(self, x, y, rgb_image):
        if x < 0 or x >= rgb_image.height or y < 0 or y >= rgb_image.height:
            return 0
        r, g, b = rgb_image.getpixel((x, y))
        height = r+g+b
        height -= self.__MAX_PIXEL_COLOUR / 2
        height /= self.__MAX_PIXEL_COLOUR / 2
        height *= self.__MAX_HEIGHT
        return height

    @staticmethod
    def getSize():
        return Terrain.__SIZE
