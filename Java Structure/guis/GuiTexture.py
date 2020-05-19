class GuiTexture:
    def __init__(self, texture, position, scale):
        self.texture = texture
        self.position = position
        self.scale = scale

    def getTexture(self):
        return self.texture

    def getPosition(self):
        return self.position

    def getScale(self):
        return self.scale