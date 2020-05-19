import models.TexturedModel

class Entity:
    # Creates a new ...
    # *
    # * (TexturedModel) model
    # * (Vector3) position
    # * (float) rotX, rotY, rotZ
    # * (float) scale
    # * (int) textureIndex -> TextureAtlas
    def __init__(self, model, position, rotX, rotY, rotZ, scale, textureIndex=0):
        self.model = model
        self.position = Vector3(position)
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scale = scale
        self.textureIndex = textureIndex

    def getTextureXOffset(self):
        column = self.textureIndex % self.model.getTexture().getNumberOfRows()
        return column / self.model.getTexture.getNumberOfRows()

    def getTextureYOffset(self):
        row = self.textureIndex // self.model.getTexture().getNumberOfRows()
        return row / self.model.getTexture().getNumberOfRows()

    def increasePosition(self, dx, dy, dz):
        self.position.x += dx
        self.position.y += dy
        self.position.z += dz

    def increaseRotation(self, dx, dy, dz):
        self.rotX += dx
        self.rotY += dy
        self.rotZ += dz

    def getModel(self):
        return self.model