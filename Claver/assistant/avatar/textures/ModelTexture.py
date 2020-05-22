class ModelTexture:
    def __init__(self, id):
        self.__textureID = id
        self.__shineDamper = 1
        self.__reflectivity = 0

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