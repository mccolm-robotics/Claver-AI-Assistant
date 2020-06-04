from pyrr import Vector3


class Entity:
    def __init__(self, model, position, rotX, rotY, rotZ, scale):
        self.__model = model
        self.__position = Vector3(position)
        self.__rotX = rotX
        self.__rotY = rotY
        self.__rotZ = rotZ
        self.__scale = scale

    def increasePosition(self, dx, dy, dz):
        self.__position.x += dx
        self.__position.y += dy
        self.__position.z += dz

    def increaseRotation(self, dx, dy, dz):
        print(dx, dy, dz)
        self.__rotX += dx
        self.__rotY += dy
        self.__rotZ += dz

    def getModel(self):
        return self.__model

    def setModel(self, model):
        self.__model = model

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = Vector3(position)

    def setRotation(self, dx, dy, dz):
        self.__rotX = dx
        self.__rotY = dy
        self.__rotZ = dz

    def getRotX(self):
        return self.__rotX

    def setRotX(self, rotX):
        self.__rotX = rotX

    def getRotY(self):
        return self.__rotY

    def setRotY(self, rotY):
        self.__rotY = rotY

    def getRotZ(self):
        return self.__rotZ

    def setRotZ(self, rotZ):
        self.__rotZ = rotZ

    def getScale(self):
        return self.__scale

    def setScale(self, scale):
        self.__scale = scale

    def __str__(self):
        return "Entity (position:{} rotx:{} roty:{} rotz:{} scale:{}".format(self.__position, self.__rotX, self.__rotY, self.__rotZ, self.__scale)
