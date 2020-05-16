class TexturedModel:
    def __str__(self, model, texture):
        self.modelData = model
        self.texture = texture

    def getModelData(self):
        return self.modelData

    def getTexture(self):
        return self.texture