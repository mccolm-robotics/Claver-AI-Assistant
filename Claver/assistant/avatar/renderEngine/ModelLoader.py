from Claver.assistant.avatar.renderEngine.Loader import Loader
from pyassimp import *

class ModelLoader:
    def __init__(self):
        self.__vertices = None
        self.__normals = None
        self.__textures = None

    def loadModel(self, fileName, loader):
        print("hello world")
        self.scene = load(fileName)
        model = self.scene.meshes[0]
        self.__vertices = model.vertices
        self.__normals = model.normals
        self.__textures = model.texturecoords[0]
        release(self.scene)
        return loader.loadToVAO(self.__vertices, self.__textures, self.__normals)


        # self.scene = load('models/char_01_triangulated.obj')
        # self.blenderModel = self.scene.meshes[0]
        # print("Name of model being loaded: ", self.blenderModel)
        # self.model = np.concatenate(
        #     (self.blenderModel.vertices, self.blenderModel.normals, self.blenderModel.texturecoords[0]), axis=0)
        #
        # self.vertices_offset = 0
        # self.normal_offset = self.model.itemsize * len(self.blenderModel.vertices) * 3
        # self.texture_offset = self.normal_offset + (self.model.itemsize * len(
        # self.blenderModel.texturecoords[0]) * 3)  # Assimp represents the texture as a vec3 (u, v, 0)
        #
        # glVertexAttribPointer(self.vertexLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.vertices_offset))
        #
        # # Describe the position data layout in the buffer
        # glEnableVertexAttribArray(self.textureLocationInShader)
        # glVertexAttribPointer(self.textureLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.texture_offset))
        #
        # glEnableVertexAttribArray(self.normalLocationInShader)
        # glVertexAttribPointer(self.normalLocationInShader, 3, GL_FLOAT, GL_FALSE, self.model.itemsize * 3, ctypes.c_void_p(self.normal_offset))
