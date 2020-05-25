import numpy as np
from pyrr import Vector3

class Terrain:
    __SIZE = 80              # How many unit lengths long?
    __VERTEX_COUNT = 128      # How many sections to break the terrain into

    def __init__(self, gridX, gridZ, loader, texture):
        self.__texture = texture
        self.__x = gridX * self.__SIZE
        self.__z = gridZ * self.__SIZE
        self.__model = self.__generateTerrain(loader)

    def getX(self):
        return self.__x

    def getZ(self):
        return self.__z

    def getModel(self):
        return self.__model

    def getTexture(self):
        return self.__texture

    def __generateTerrain(self, loader):
        vertices = []
        normals = []
        textureCoords = []
        for i in range(self.__VERTEX_COUNT):
            for j in range(self.__VERTEX_COUNT):
                vertices.append(Vector3([j / (self.__VERTEX_COUNT - 1) * self.__SIZE, 0, i / (self.__VERTEX_COUNT - 1) * self.__SIZE]))
                normals.append(Vector3([0.0, 1.0, 0.0]))
                textureCoords.append(Vector3([j / (self.__VERTEX_COUNT - 1), i / (self.__VERTEX_COUNT - 1), 0.0]))

        indices = []
        for gz in range(self.__VERTEX_COUNT - 1):
            for gx in range(self.__VERTEX_COUNT - 1):
                topLeft = (gz * self.__VERTEX_COUNT) + gx;
                topRight = topLeft + 1;
                bottomLeft = ((gz + 1) * self.__VERTEX_COUNT) + gx;
                bottomRight = bottomLeft + 1;
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

