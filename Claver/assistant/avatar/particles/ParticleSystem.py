from pyrr import Vector3, vector3, Vector4, matrix44
import random
from math import pi, cos, sin, sqrt, acos, floor
from Claver.assistant.avatar.particles.Particle import Particle


class ParticleSystem:

    def __init__(self, texture, pps, speed, gravityComplient, lifeLength):
        self.__pps = pps
        self.__speed = speed
        self.__gravityComplient = gravityComplient
        self.__lifeLength = lifeLength
        self.__texture = texture

    def generateParticles(self, systemCenter, delta):
        particlesToCreate = self.__pps * delta
        count = floor(particlesToCreate)
        partialParticle = particlesToCreate % 1
        for i in range(count):
            self.__emitParticle(systemCenter)
        if random.random() < partialParticle:
            self.__emitParticle(systemCenter)

    def __emitParticle(self, center):
        dirX = random.random() * 2.0 - 1.0
        dirZ = random.random() * 2.0 - 1.0
        velocity = Vector3((dirX, 1.0, dirZ))
        velocity = vector3.normalize(velocity)
        velocity = velocity * self.__speed
        Particle(self.__texture, center, velocity, self.__gravityComplient, self.__lifeLength, 0.0, 1.0)

