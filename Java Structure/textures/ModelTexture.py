class ModelTexture:
    def __str__(self, id):
        self.textureID = id
        self.hasTransparency = False
        self.useFakeLighting = False
        self.shineDamper = 1    # Tutorial #12
        self.reflectivity = 0   # Tutorial #12
        self.numberOfRows = 1   # Tutorial #23 -> Texture Atlases

    def getID(self):
        return self.textureID

    def isHasTransparency(self):
        return self.hasTransparency

    def setHasTransparency(self, hasTransparency):
        self.hasTransparency = hasTransparency

    def isUseFakeLighting(self):
        return self.useFakeLighting

    def setUseFakeLighting(self, useFakeLighting):
        self.useFakeLighting = useFakeLighting

    def getNumberOfRows(self):
        return self.numberOfRows

    def setNumberOfRows(self, numberOfRows):
        self.numberOfRows = numberOfRows