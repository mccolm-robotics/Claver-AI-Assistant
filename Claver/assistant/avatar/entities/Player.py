from Claver.assistant.avatar.entities.Entity import Entity
from math import sin, cos, radians


class Player(Entity):
    __RUN_SPEED = 10  # units / sec
    __TURN_SPEED = 160  # deg / sec

    def __init__(self, model, position, rotX, rotY, rotZ, scale, inputEvents):
        super().__init__(model, position, rotX, rotY, rotZ, scale)
        self.__inputEvents = inputEvents
        self.__currentSpeed = 0
        self.__currentTurnSpeed = 0

    def move(self, delta):
        self.checkInputs()
        print("Turn Speed: ", self.__currentTurnSpeed)
        super().increaseRotation(0, 1, 0)
        distance = self.__currentSpeed * delta / 1000000
        dx = distance * sin(radians(super().getRotY()))
        dz = distance * cos(radians(super().getRotY()))
        # print("Distance:{} RotY:{} radians(super().getRotY()): {} cos(radians(super().getRotY())):{}".format(distance, super().getRotY(), radians(super().getRotY()), cos(radians(super().getRotY()))))
        super().increasePosition(dx, 0, dz)

    def checkInputs(self):
        if self.__inputEvents.isKeyDown('w') is True and self.__inputEvents.isKeyDown('s') is False:
            self.__currentSpeed = self.__RUN_SPEED
        elif self.__inputEvents.isKeyDown('s') is True and self.__inputEvents.isKeyDown('w') is False:
            self.__currentSpeed = -self.__RUN_SPEED
        else:
            self.__currentSpeed = 0

        if self.__inputEvents.isKeyDown('d') is True and self.__inputEvents.isKeyDown('a') is False:
            self.__currentTurnSpeed = -self.__TURN_SPEED
        elif self.__inputEvents.isKeyDown('a') is True and self.__inputEvents.isKeyDown('d') is False:
            self.__currentTurnSpeed = self.__TURN_SPEED
        else:
            self.__currentTurnSpeed = 0
