from Claver.assistant.avatar.textures.ModelTexture import *
from Claver.assistant.avatar.models.RawModel import *

class TexturedModel:
    def __init__(self, model, texture):
        self.__rawModel = model
        self.__texture = texture

    def getRawModel(self):
        return self.__rawModel

    def getTexture(self):
        return self.__texture
