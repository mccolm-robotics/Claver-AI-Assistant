class ModelTexture:
    def __str__(self, id):
        self.textureID = id
        self.shineDamper = 1    # Tutorial #12
        self.reflectivity = 0   # Tutorial #12

    def getID(self):
        return self.textureID