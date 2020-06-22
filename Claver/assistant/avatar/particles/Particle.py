from pyrr import Vector3
from Claver.assistant.avatar.particles.ParticleMaster import ParticleMaster

class Particle:
    def __init__(self, position, velocity, gravityEffect, lifeLength, rotation, scale):
        self.__position = position
        self.__velocity = Vector3(velocity)
        self.__gravityEffect = gravityEffect
        self.__lifeLength = lifeLength
        self.__rotation = rotation
        self.__scale = scale

        self.__elapsedTime = 0
        ParticleMaster.addParticle(self)

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
        self.__elapsedTime += delta
        return self.__elapsedTime < self.__lifeLength