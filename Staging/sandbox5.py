particles_dict = {}


class TextureObject:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name


class ParticleObject:
    def __init__(self, name):
        self.name = name
        self.status = True

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status


texture_1 = TextureObject(1)
texture_2 = TextureObject(2)

particle_1 = ParticleObject(1)
particle_2 = ParticleObject(2)

particles_dict[texture_1] = [particle_1]


# print(particles_dict)

for particleTextureList in particles_dict:
    print(particleTextureList)
    for particle in particles_dict[particleTextureList]:
        print(particle.getName())
        # stillAlive = particle.getStatus()
        # if not stillAlive:
        #     particleTextureList.remove(particle)
        #     if not particleTextureList:
        #         del particles_dict[particleTextureList]
