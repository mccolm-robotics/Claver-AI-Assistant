class FontType:
    def __init__(self, textureAtlas, fontFile, window_rect):
        from Claver.assistant.avatar.fontMeshCreator.TextMeshCreator import TextMeshCreator
        self.__textureAtlas = textureAtlas
        self.__loader = TextMeshCreator(fontFile, window_rect)

    def getTextureAtlas(self):
        return self.__textureAtlas

    def loadText(self, text):
        return self.__loader.createTextMesh(text)