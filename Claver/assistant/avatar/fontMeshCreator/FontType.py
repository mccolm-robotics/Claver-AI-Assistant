from Claver.assistant.avatar.fontMeshCreator.TextMeshCreator import TextMeshCreator

class FontType:
    def __init__(self, textureAtlas, fontFile):
        self.__textureAtlas = textureAtlas
        self.__loader = TextMeshCreator(fontFile)

    def getTextureAtlas(self):
        return self.__textureAtlas

    def loadText(self, text):
        return self.__loader.createTextMesh(text)