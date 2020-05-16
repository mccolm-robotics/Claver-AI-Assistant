class MasterRenderer:
    def __init__(self):
        self.shader = StaticShader()
        self.renderer = Renderer(self.shader)
        self.entities = {}

    # Creates a new ...
    # *
    # * (Light) sun
    # * (Camera) camera
    def render(self, sun, camera):
        self.renderer.prepare()
        self.shader.start()
        self.shader.loadLight(sun)
        self.shader.loadViewMatrix(camera)
        self.renderer.render(self.entities)
        self.shader.stop()
        self.entities.clear()

    def processEntity(self, entity):
        entityModel = entity.getModel()
        if entityModel in self.entities:
            self.entities[entityModel].append(entity)
        else:
            self.entities[entityModel] = [entity]


    def cleanUp(self):
        self.shader.cleanUp()