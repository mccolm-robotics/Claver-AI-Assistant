import ShaderProgram

class StaticShader(ShaderProgram):
    def __index__(self, vertexFile, fragmentFile):
        super().__init__(vertexFile, fragmentFile)

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoords")
        super().bindAttribute(2, "normal")


    def getAllUniformLocations(self):
        self.location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.location_lightPosition = super().getUniformLocation("lightPosition")
        self.location_lightColour = super().getUniformLocation("lightColour")
        self.location_shineDamper = super().getUniformLocation("shineDamper")
        self.location_reflectivity = super().getUniformLocation("reflectivity")

    def loadShineVariables(self, damper, reflectivity):
        super.loadFloat(self.location_shineDamper, damper)
        super.loadFloat(self.location_reflectivity, reflectivity)

    def loadTransformationMatrix(self, matrix):
        super.loadMatrix(self.location_transformationMatrix, matrix)

    def loadLight(self, light):
        super.loadVector(self.location_lightPosition, light.getPosition())
        super.loadVector(self.location_lightColour, light.getColour())

    def loadViewMatrix(self, camera):
        viewMatrix = Math.createViewMatrix(camera)
        super.loadMatrix(self.location_viewMatrix, viewMatrix)

    def loadProjectionMatrix(self, projection):
        super.loadMatrix(self.location_projectionMatrix, projection)