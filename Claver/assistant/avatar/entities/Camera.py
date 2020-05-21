from pyrr import Vector3

class Camera:
    __MOVEMENT_SPEED = 0.002

    def __init__(self):
        self.__position = Vector3((0.0, 5.0, 18))
        self.__pitch = None
        self.__yaw = None
        self.__roll = None

    def move(self, keyboardEvent):
        if keyboardEvent.isKeyDown('w'):
            self.__position.z -= self.__MOVEMENT_SPEED
        if keyboardEvent.isKeyDown('s'):
            self.__position.z += self.__MOVEMENT_SPEED
        if keyboardEvent.isKeyDown('d'):
            self.__position.x += self.__MOVEMENT_SPEED
        if keyboardEvent.isKeyDown('a'):
            self.__position.x -= self.__MOVEMENT_SPEED

    def getPosition(self):
        return self.__position

    def getPitch(self):
        return self.__pitch

    def getYaw(self):
        return self.__yaw

    def getRoll(self):
        return self.__roll
