import pyrr

from Claver.assistant.avatar.entities.Entity import Entity
from math import sin, cos, radians, floor
from pyrr import Vector3

from assistant.avatar.terrain.Terrain import Terrain


class Player(Entity):
    __RUN_SPEED = 10  # units / sec
    __SIDE_STEP_SPEED = __RUN_SPEED  # units / sec
    __GRAVITY = -17
    __JUMP_POWER = 7
    __TERRAIN_HEIGHT = 0


    def __init__(self, model, position, rotX, rotY, rotZ, scale, inputEvents, terrainTiles):
        super().__init__(model, position, rotX, rotY, rotZ, scale)
        self.__inputEvents = inputEvents
        self.__currentSpeed = 0
        self.__currentSideStepSpeed = 0
        self.__upwardsSpeed = 0
        self.__isInAir = False
        self.__terrainTiles = terrainTiles
        self.ground = self.__TERRAIN_HEIGHT

    def move(self, delta, sideStepDirection, yaw=None):

        self.__checkInputs()
        if yaw is not None:
            super().setRotY(yaw)
        else:
            yaw = super().getRotY()

        runDistance = self.__currentSpeed * delta
        sideStepDistance = self.__currentSideStepSpeed * delta

        super().setPosition(super().getPosition() - (sideStepDirection * sideStepDistance))

        dx = runDistance * sin(yaw)
        dz = runDistance * cos(yaw)
        super().increasePosition(dx, 0, dz)
        self.__upwardsSpeed += self.__GRAVITY * delta
        super().increasePosition(0, self.__upwardsSpeed * delta, 0)

        gridX = super().getPosition().x / Terrain.getSize()
        gridZ = super().getPosition().z / Terrain.getSize()
        tileX = int((gridX + 1) // 1)
        tileZ = int((gridZ + 1) // 1)
        # print("ID:{} tileX:{} tileZ:{}".format(self.__terrainTiles[tileX][tileZ].getID(), tileX, tileZ))
        self.ground = self.__terrainTiles[tileX][tileZ].getHeightOfTerrain(super().getPosition().x, super().getPosition().z)

        if super().getPosition().y < self.ground:
            self.__upwardsSpeed = 0
            super().setYPosition(self.ground)
            self.__isInAir = False

        # print("tileX:{} tileZ:{}".format(tileX, tileZ))
        # print("X:{} Z:{}".format(int(super().getPosition().x), int(super().getPosition().z)))


    def __jump(self):
        if self.__isInAir is False:
            self.__upwardsSpeed = self.__JUMP_POWER
            self.__isInAir = True

    def __checkInputs(self):
        if self.__inputEvents.isKeyDown('w') is True and self.__inputEvents.isKeyDown('s') is False:
            self.__currentSpeed = self.__RUN_SPEED
        elif self.__inputEvents.isKeyDown('s') is True and self.__inputEvents.isKeyDown('w') is False:
            self.__currentSpeed = -self.__RUN_SPEED
        else:
            self.__currentSpeed = 0

        if self.__inputEvents.isKeyDown('d'):
            self.__currentSideStepSpeed = self.__SIDE_STEP_SPEED
        elif self.__inputEvents.isKeyDown('a'):
            self.__currentSideStepSpeed = -self.__SIDE_STEP_SPEED
        else:
            self.__currentSideStepSpeed = 0

        if self.__inputEvents.isKeyDown('space'):
            self.__jump()

    def getPosition(self):
        return super().getPosition()

    def getRunSpeed(self):
        return self.__RUN_SPEED

    def getGroundHeight(self):
        return self.ground