class Terrain:
    __SIZE = 80
    __VERTEX_COUNT = 128

    def __init__(self, gridX, gridZ, loader, texture):
        self.__x = gridX * self.__SIZE
        self.__z = gridZ * self.__SIZE
        self.__model = None
        self.__texture = texture

    def __generateTerrain(self, loader):
        count = self.__VERTEX_COUNT * self.__VERTEX_COUNT
        vertices = []
        normals = []
        textureCoords = []
        vertexPointer = 0
        for i in range(self.__VERTEX_COUNT):
            for j in range(self.__VERTEX_COUNT):
                vertices[vertexPointer * 3] = j/(self.__VERTEX_COUNT - 1) * self.__SIZE
                vertices[vertexPointer * 3 + 1] = 0
                vertices[vertexPointer * 3 + 2] = i/(self.__VERTEX_COUNT - 1) * self.__SIZE
                normals[vertexPointer * 3] = 0
                normals[vertexPointer * 3 + 1] = 1
                normals[vertexPointer * 3 + 2] = 0
                textureCoords[vertexPointer * 3] = j/(self.__VERTEX_COUNT - 1)
                textureCoords[vertexPointer * 3 + 1] = i/(self.__VERTEX_COUNT - 1)
                textureCoords[vertexPointer * 3 + 2] = 0.0
                vertexPointer+=1
        return loader.loadToVAO(vertices, textureCoords, normals);
