import numpy as np
from pyrr import Vector3

class Primitives:
    def __init__(self):
        pass

    def cube(self):
        vertices = [
            -1.0, 1.0, 1.0,  # Left
            -1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0,
            -1.0, 1.0, 1.0,

            1.0, 1.0, 1.0,  # Front
            -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0,
            -1.0, 1.0, 1.0,
            -1.0, -1.0, 1.0,
            1.0, 1.0, 1.0,

            1.0, 1.0, -1.0,  # Back
            -1.0, -1.0, -1.0,
            -1.0, 1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, 1.0, -1.0,

            1.0, 1.0, -1.0,  # Right
            1.0, -1.0, 1.0,
            1.0, -1.0, -1.0,
            1.0, 1.0, 1.0,
            1.0, -1.0, 1.0,
            1.0, 1.0, -1.0,

            1.0, 1.0, -1.0,  # Top
            -1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0,
            -1.0, 1.0, 1.0,
            1.0, 1.0, -1.0,

            1.0, -1.0, 1.0,  # Bottom
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, 1.0,

        ]

        textureCoords = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,

            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,

            0.0, 0.0, 0.0,
            1.0, 1.0, 0.0,
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,

            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,

            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 0.0, 0.0,

            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 1.0, 0.0,
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            1.0, 0.0, 0.0
        ]

        normals = [
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,

            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,

            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,

            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0
        ]

        return dict(vertices=vertices, textureCoords=textureCoords, normals=normals)

    def terrain(self):
        vertices = []
        normals = []
        textureCoords = []
        VERTEX_COUNT = 4
        SIZE = 3

        for i in range(VERTEX_COUNT):
            for j in range(VERTEX_COUNT):
                vertices.append(Vector3([j / (VERTEX_COUNT - 1) * SIZE, 0, i / (VERTEX_COUNT - 1) * SIZE]))
                normals.append(Vector3([0.0, 1.0, 0.0]))
                textureCoords.append(Vector3([j / (VERTEX_COUNT - 1), i / (VERTEX_COUNT - 1), 0.0]))

        indices = []
        for gz in range(VERTEX_COUNT - 1):
            for gx in range(VERTEX_COUNT - 1):
                topLeft = (gz * VERTEX_COUNT) + gx;
                topRight = topLeft + 1;
                bottomLeft = ((gz + 1) * VERTEX_COUNT) + gx;
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

        return dict(vertices=finalVertexList, textureCoords=finalTextCoordsList, normals=finalNormalList)
