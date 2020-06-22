class ParticleMaster:

    __particles = []
    __renderer = None

    @staticmethod
    def init(loader, projectionMatrix, camera):
        from Claver.assistant.avatar.particles.ParticleRenderer import ParticleRenderer
        ParticleMaster.__renderer = ParticleRenderer(loader, projectionMatrix, camera)

    @staticmethod
    def update():
        for particle in ParticleMaster.__particles:
            stillAlive = particle.update()
            if not stillAlive:
                ParticleMaster.__particles.remove(particle)

    @staticmethod
    def renderParticles():
        ParticleMaster.__renderer.render(ParticleMaster.__particles)

    @staticmethod
    def cleanUp():
        ParticleMaster.__renderer.cleanUp()

    @staticmethod
    def addParticle(particle):
        ParticleMaster.__particles.append(particle)