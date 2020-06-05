from Claver.assistant.avatar.entities.Entity import Entity
from math import sin, cos, radians
from pyrr import Vector3


class Player(Entity):
    __RUN_SPEED = 10  # units / sec
    __TURN_SPEED = 2.5  # radians / sec
    __GRAVITY = -17
    __JUMP_POWER = 7
    __TERRAIN_HEIGHT = 0


    def __init__(self, model, position, rotX, rotY, rotZ, scale, inputEvents):
        super().__init__(model, position, rotX, rotY, rotZ, scale)
        self.__inputEvents = inputEvents
        self.__currentSpeed = 0
        self.__currentTurnSpeed = 0
        self.__upwardsSpeed = 0
        self.__isInAir = False

    def move(self, delta):
        delta = delta / 1000000
        self.__checkInputs(delta)
        super().increaseRotation(0, -self.__currentTurnSpeed * delta, 0)
        distance = self.__currentSpeed * delta
        dx = distance * sin(super().getRotY())
        dz = distance * cos(super().getRotY())
        super().increasePosition(dx, 0, dz)
        self.__upwardsSpeed += self.__GRAVITY * delta
        super().increasePosition(0, self.__upwardsSpeed * delta, 0)
        if super().getPosition().y < self.__TERRAIN_HEIGHT:
            self.__upwardsSpeed = 0
            super().setYPosition(self.__TERRAIN_HEIGHT)
            self.__isInAir = False

    def __jump(self):
        if self.__isInAir is False:
            self.__upwardsSpeed = self.__JUMP_POWER
            self.__isInAir = True

    def __checkInputs(self, delta):
        if self.__inputEvents.isKeyDown('w') is True and self.__inputEvents.isKeyDown('s') is False:
            self.__currentSpeed = self.__RUN_SPEED
        elif self.__inputEvents.isKeyDown('s') is True and self.__inputEvents.isKeyDown('w') is False:
            self.__currentSpeed = -self.__RUN_SPEED
        else:
            self.__currentSpeed = 0

        if self.__inputEvents.isKeyDown('d') is True and self.__inputEvents.isKeyDown('a') is False:
            self.__currentTurnSpeed = self.__TURN_SPEED
        elif self.__inputEvents.isKeyDown('a') is True and self.__inputEvents.isKeyDown('d') is False:
            self.__currentTurnSpeed = -self.__TURN_SPEED
        else:
            self.__currentTurnSpeed = 0

        if self.__inputEvents.isKeyDown('space'):
            self.__jump()
            # super().increasePosition(0, self.__upwardsSpeed * delta, 0)

    def getPosition(self):
        return super().getPosition()