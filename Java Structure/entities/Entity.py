import models.TexturedModel

class Entity:
    # Creates a new ...
    # *
    # * (TexturedModel) model
    # * (Vector3) position
    # * (float) rotX, rotY, rotZ
    # * (float) scale
    def __init__(self, model, position, rotX, rotY, rotZ, scale):
        self.model = model
        self.position = Vector3(position)
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scale = scale

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