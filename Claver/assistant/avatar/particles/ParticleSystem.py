from pyrr import Vector3, vector3, Vector4, matrix44
import random
from math import pi, cos, sin, sqrt, acos, floor
from Claver.assistant.avatar.particles.Particle import Particle

class ParticleSystem:
    def __init__(self, pps, speed, gravityComplient, lifeLength, scale):
        self.__pps = pps
        self.__averageSpeed = speed
        self.__gravityComplient = gravityComplient
        self.__averageLifeLength = lifeLength
        self.__averageScale = scale
        self.__speedError = 0
        self.__lifeError = 0
        self.__scaleError = 0
        self.__randomRotation = False
        self.__directionDeviation = 0
        self.__direction = None
        
    # direction - The average direction in which particles are emitted.
    # deviation - A value between 0 and 1 indicating how far from the chosen direction particles can deviate.
    def setDirection(self, direction, deviation):
        self.__direction = Vector3((direction[0], direction[1], direction[2]))
        self.__directionDeviation = deviation * pi

    def randomizeRotation(self):
        self.__randomRotation = True

    # error - A number between 0 and 1, where 0 means no error margin
    def setSpeedError(self, error):
        self.__speedError = error * self.__averageSpeed

    # error - A number between 0 and 1, where 0 means no error margin
    def setLifeError(self, error):
        self.__lifeError = error * self.__averageLifeLength

    # error - A number between 0 and 1, where 0 means no error margin
    def setScaleError(self, error):
        self.__scaleError = error * self.__averageScale

    def generateParticles(self, delta, systemCenter):
        particlesToCreate = self.__pps * delta
        count = floor(particlesToCreate)
        partialParticle = particlesToCreate % 1
        for i in range(count):
            self.__emitParticle(systemCenter)
        if random.random() < partialParticle:
            self.__emitParticle(systemCenter)


    def __emitParticle(self, center):
        velocity = None
        if self.__direction is not None:
            velocity = ParticleSystem.__generateRandomUnitVectorWithinCone(self.__direction, self.__directionDeviation)
        else:
            velocity = self.__generateRandomUnitVector()
        velocity = vector3.normalize(velocity)
        velocity *= self.__generateValue(self.__averageSpeed, self.__speedError)
        scale = self.__generateValue(self.__averageScale, self.__scaleError)
        lifeLength = self.__generateValue(self.__averageLifeLength, self.__lifeError)
        Particle(center, velocity, self.__gravityComplient, lifeLength, self.__generateRotation(), scale)

    def __generateValue(self, average, errorMargin):
        offset = (random.uniform(0.0, 1.0) - 0.5) * 2 * errorMargin
        return average + offset

    def __generateRotation(self):
        if self.__randomRotation:
            return random.uniform(0.0, 1.0) * 360
        else:
            return 0

    @staticmethod
    def __generateRandomUnitVectorWithinCone(coneDirection, angle):
        coneDirection = Vector3(coneDirection)
        cosAngle = cos(angle)
        theta = random.uniform(0.0, 1.0) * 2 * pi
        z = cosAngle + (random.uniform(0.0, 1.0) * (1 - cosAngle))
        rootOneMinusZSquared = sqrt(1 - z * z)
        x = rootOneMinusZSquared * cos(theta)
        y = rootOneMinusZSquared * sin(theta)

        direction = Vector4((x, y, z, 1))
        # Check if coneDirection is z-axis
        if coneDirection.x != 0 or coneDirection.y != 0 or (coneDirection.z != 1 and coneDirection.z != -1):
            rotateAxis = vector3.cross(coneDirection, (0, 0, 1))
            rotateAxis = vector3.normalize(rotateAxis)
            rotateAngle = acos(vector3.dot(coneDirection, (0, 0, 1)))
            rotationMatrix = matrix44.create_from_axis_rotation(rotateAxis, -rotateAngle)
            direction = Vector4(matrix44.apply_to_vector(rotationMatrix, direction))
        elif coneDirection.z == -1:
            direction.z *= -1
        return (direction.x, direction.y, direction.z)

    def __generateRandomUnitVector(self):
        theta = random.uniform(0.0, 1.0) * 2 * pi
        z = (random.uniform(0.0, 1.0) * 2) - 1
        rootOneMinusZSquared = sqrt(1 - z * z)
        x = rootOneMinusZSquared * cos(theta)
        y = rootOneMinusZSquared * sin(theta)
        return (x, y, z)
