import models.ModelData

class ModelLoader:
    # Creates a new...
    # *
    # * (String) fileName
    # * (Loader) loader
    def __init__(self, fileName, loader):
        pyassimp functions to load model
        self.vertices = []
        self.textures = []
        self.normals = []
        verticesArray = []
        textureArray = []
        self.loader = loader

    def loadModel(self):
        return self.loader.loadToVAO(verticesArray, textureArray, normalsArray)
