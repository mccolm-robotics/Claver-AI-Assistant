from pyrr import Vector3
from math import floor
from Claver.assistant.avatar.particles.ParticleMaster import ParticleMaster
from Claver.assistant.avatar.entities.Camera import Camera

class Particle:
    def __init__(self, texture, position, velocity, gravityEffect, lifeLength, rotation, scale):
        self.__texture = texture
        self.__position = position
        self.__velocity = Vector3(velocity)
        self.__gravityEffect = gravityEffect
        self.__lifeLength = lifeLength
        self.__rotation = rotation
        self.__scale = scale

        self.__elapsedTime = 0
        self.__texOffset1 = [0, 0]
        self.__texOffset2 = [0, 0]
        self.__blend = 0
        self.__distance = 0
        ParticleMaster.addParticle(self)

    def getDistance(self):
        return self.__distance

    def getTexOffset1(self):
        return self.__texOffset1

    def getTexOffset2(self):
        return self.__texOffset2

    def getBlend(self):
        return self.__blend

    def getTexture(self):
        return self.__texture

    def getPosition(self):
        return self.__position

    def getRotation(self):
        return self.__rotation

    def getScale(self):
        return self.__scale

    def update(self, delta):
        from Claver.assistant.avatar.entities.Player import Player
        self.__velocity.y += Player.GRAVITY * self.__gravityEffect * delta
        change = Vector3((self.__velocity.x, self.__velocity.y, self.__velocity.z)) # create a copy by value - not by reference
        change *= delta     # scale vector
        self.__position += change   # add two vectors together

        self.__updateTextureCoordInfo()
        self.__elapsedTime += delta
        return self.__elapsedTime < self.__lifeLength

    def __updateTextureCoordInfo(self):
        lifeFactor = self.__elapsedTime / self.__lifeLength
        stageCount = self.__texture.getNumberOfRows() * self.__texture.getNumberOfRows()
        atlasProgression = lifeFactor * stageCount
        index1 = floor(atlasProgression)
        index2 = index1 + 1 if index1 < (stageCount - 1) else index1
        self.__blend = atlasProgression % 1
        self.__setTextureOffset(self.__texOffset1, index1)
        self.__setTextureOffset(self.__texOffset2, index2)
        # print("texOffset1: {} and texOffset2: {}".format(self.__texOffset1, self.__texOffset2))

    def __setTextureOffset(self, offset, index):
        column = index % self.__texture.getNumberOfRows()
        row = index // self.__texture.getNumberOfRows()
        offset[0] = column / self.__texture.getNumberOfRows()
        offset[1] = row / self.__texture.getNumberOfRows()