from pyrr import Vector3, vector3, Vector4, matrix44
import random
from math import pi, cos, sin, sqrt, acos, floor
from Claver.assistant.avatar.particles.Particle import Particle


class ParticleSystem:

    def __init__(self, texture, pps, speed, gravityComplient, lifeLength, scale=1):
        self.__pps = pps
        self.__averageSpeed = speed
        self.__gravityComplient = gravityComplient
        self.__averageLifeLength = lifeLength
        self.__texture = texture
        self.__averageScale = scale

        self.__randomRotation = False
        self.__speedError = 0
        self.__lifeError = 0
        self.__scaleError = 0
        self.__direction = None
        self.__directionDeviation = 0

    def setDirection(self, direction, deviation):
        self.__direction = direction
        self.__directionDeviation = deviation * pi

    def randomizeRotation(self):
        self.__randomRotation = True

    def setSpeedError(self, error):
        self.__speedError = error * self.__averageSpeed

    def setLifeError(self, error):
        self.__lifeError = error * self.__averageLifeLength

    def setScaleError(self, error):
        self.__scaleError = error * self.__averageScale

    def generateParticles(self, systemCenter, delta):
        particlesToCreate = self.__pps * delta
        count = floor(particlesToCreate)
        partialParticle = particlesToCreate % 1
        for i in range(count):
            self.__emitParticle(systemCenter)
        if random.random() < partialParticle:
            self.__emitParticle(systemCenter)

    def __emitParticle(self, center):
        if self.__direction is not None:
            velocity = ParticleSystem.__generateRandomUnitVectorWithinCone(self.__direction, self.__directionDeviation)
        else:
            velocity = self.__generateRandomUnitVector()
        velocity = vector3.normalize(velocity)
        velocity *= (self.__generateValue(self.__averageSpeed, self.__speedError))
        scale = self.__generateValue(self.__averageScale, self.__scaleError)
        lifeLength = self.__generateValue(self.__averageLifeLength, self.__lifeError)
        Particle(self.__texture, center, velocity, self.__gravityComplient, lifeLength, self.__generateRotation(), scale)

    def __generateValue(self, average, errorMargin):
        offset = (random.uniform(0, 1) - 0.5) * 2.0 * errorMargin
        return average + offset

    def __generateRotation(self):
        if self.__randomRotation is True:
            return (random.uniform(0, 1) * 360.0)
        else:
            return 0

    @staticmethod
    def __generateRandomUnitVectorWithinCone(coneDirection, angle):
        cosAngle = cos(angle)
        theta = random.uniform(0, 1) * 2 * pi
        z = cosAngle + (random.uniform(0, 1) * (1 - cosAngle))
        rootOneMinusZSquared = sqrt(1 - z * z)
        x = rootOneMinusZSquared * cos(theta)
        y = rootOneMinusZSquared * sin(theta)

        direction = [x, y, z, 1.0]
        if coneDirection[0] != 0 or coneDirection[1] != 0 or (coneDirection[2] != 1 and coneDirection[2] != -1):
            rotateAxis = vector3.cross(coneDirection, (0.0, 0.0, 1.0))
            rotateAxis = vector3.normalize(rotateAxis)
            rotateAngle = acos(vector3.dot(coneDirection, (0.0, 0.0, 1.0)))
            rotationMatrix = matrix44.create_from_axis_rotation(rotateAxis, -rotateAngle)
            direction = matrix44.apply_to_vector(rotationMatrix, direction)
        elif coneDirection[2] == -1:
            direction[2] *= -1
        return (direction[0], direction[1], direction[2])

    def __generateRandomUnitVector(self):
        theta = random.uniform(0, 1) * 2 * pi
        z = (random.uniform(0, 1) * 2) - 1
        rootOneMinusZSquared = sqrt(1 - z * z)
        x = rootOneMinusZSquared * cos(theta)
        y = rootOneMinusZSquared * sin(theta)
        return (x, y, z)

