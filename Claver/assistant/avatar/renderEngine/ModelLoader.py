from Claver.assistant.avatar.renderEngine.Loader import Loader
from pyassimp import *

class ModelLoader:
    def __init__(self):
        self.__vertices = None
        self.__normals = None
        self.__textures = None

    def loadModel(self, loader, fileName):
        self.scene = load(fileName)
        model = self.scene.meshes[0]
        self.__vertices = model.vertices
        self.__normals = model.normals
        self.__textures = model.texturecoords[0]
        release(self.scene)
        return loader.loadToVAO(self.__vertices, self.__textures, self.__normals)

    def loadPrimitive(self, loader, primitive):
        self.__vertices = primitive['vertices']
        self.__textures = primitive['textureCoords']
        self.__normals = primitive['normals']
        return loader.loadToVAO(self.__vertices, self.__textures, self.__normals)
