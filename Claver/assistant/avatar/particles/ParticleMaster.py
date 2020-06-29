from Claver.assistant.avatar.particles.InsertionSort import InsertionSort

class ParticleMaster:

    __particles_dict = {}
    __renderer = None

    @staticmethod
    def init(loader, projectionMatrix, camera):
        from Claver.assistant.avatar.particles.ParticleRenderer import ParticleRenderer
        ParticleMaster.__renderer = ParticleRenderer(loader, projectionMatrix, camera)

    @staticmethod
    def update(delta, camera):
        for particleTextureList in ParticleMaster.__particles_dict:
            for particle in ParticleMaster.__particles_dict[particleTextureList]:
                stillAlive = particle.update(delta, camera)
                if not stillAlive:
                    ParticleMaster.__particles_dict[particleTextureList].remove(particle)
                    if not ParticleMaster.__particles_dict[particleTextureList]:
                        del ParticleMaster.__particles_dict[particleTextureList]
            InsertionSort.sortHighToLow(ParticleMaster.__particles_dict[particleTextureList])

    @staticmethod
    def renderParticles():
        ParticleMaster.__renderer.render(ParticleMaster.__particles_dict)

    @staticmethod
    def cleanUp():
        ParticleMaster.__renderer.cleanUp()

    @staticmethod
    def addParticle(particle):
        if particle.getTexture() in ParticleMaster.__particles_dict:
            ParticleMaster.__particles_dict[particle.getTexture()].append(particle)
        else:
            ParticleMaster.__particles_dict[particle.getTexture()] = [particle]