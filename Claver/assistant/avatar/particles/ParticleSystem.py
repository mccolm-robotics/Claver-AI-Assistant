from pyrr import Vector3, vector3, Vector4, matrix44
import random
from math import pi, cos, sin, sqrt, acos, floor
from Claver.assistant.avatar.particles.Particle import Particle


class ParticleSystem:

    def __init__(self, pps, speed, gravityComplient, lifeLength):
        self.pps = pps
        self.speed = speed
        self.gravityComplient = gravityComplient
        self.lifeLength = lifeLength

    def generateParticles(self, systemCenter, delta):
        particlesToCreate = self.pps * delta
        count = floor(particlesToCreate)
        partialParticle = particlesToCreate % 1
        for i in range(count):
            self.emitParticle(systemCenter)
        if random.random() < partialParticle:
            self.emitParticle(systemCenter)

    def emitParticle(self, center):
        dirX = random.random() * 2.0 - 1.0
        dirZ = random.random() * 2.0 - 1.0
        velocity = Vector3((dirX, 1.0, dirZ))
        velocity = vector3.normalize(velocity)
        velocity = velocity * self.speed
        Particle(center, velocity, self.gravityComplient, self.lifeLength, 0.0, 1.0)

