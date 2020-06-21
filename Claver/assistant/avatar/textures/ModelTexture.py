class ModelTexture:
    def __init__(self, id):
        self.__textureID = id
        self.__shineDamper = 1
        self.__reflectivity = 0
        self.__hasTransparency = False
        self.__useFakeLighting = False
        self.__numberOfRows = 1
        self.__normalMap = 0

    def getNumberOfRows(self):
        return self.__numberOfRows

    def setNumberOfRows(self, numberOfRows):
        self.__numberOfRows = numberOfRows

    def getNormalMap(self):
        return self.__normalMap

    def setNormalMap(self, normalMap):
        self.__normalMap = normalMap

    def isUseFakeLighting(self):
        return self.__useFakeLighting

    def setUseFakeLighting(self, useFakeLighting):
        self.__useFakeLighting = useFakeLighting

    def isHasTransparency(self):
        return self.__hasTransparency

    def setHasTransparency(self, hasTransparency):
        self.__hasTransparency = hasTransparency

    def getID(self):
        return self.__textureID

    def getShineDamper(self):
        return self.__shineDamper

    def setShineDamper(self, shineDamper):
        self.__shineDamper = shineDamper

    def getReflectivity(self):
        return self.__reflectivity

    def setReflectivity(self, reflectivity):
        self.__reflectivity = reflectivity