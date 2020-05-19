class MasterRenderer:
    FOV = 70
    NEAR_PLANE = 0.1
    FAR_PLANE = 1000
    def __init__(self, loader):
        self.entities = {}
        self.shader = StaticShader()
        self.enableCulling()
        self.createProjectionMatrix()
        self.renderer = EntityRenderer(self.shader, self.projectionMatrix)

    def enableCulling(self):
        glEnable(GL_CULL_FACE)
        glCullFAce(GL_BACK)

    def disableCulling(self):
        glDisable(GL_CULL_Face)

    def getProjectionMatrix(self):
        return self.projectionMatrix

    def renderScene(self, entities, lights, camera, clipPlane): # All defined in his water tutorial series
        for entity in entities:
            self.processEntity(entity)
        self.render(lights, camera, clipPlane)

    # Creates a new ...
    # *
    # * ([Light]) lights
    # * (Camera) camera
    def render(self, lights, camera):
        self.prepare()
        self.shader.start()
        self.shader.loadLights(lights)
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

    def prepare(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def createProjectionMatrix(self):
        aspectRatio =
        self.projectionMatrix =

    def cleanUp(self):
        self.shader.cleanUp()