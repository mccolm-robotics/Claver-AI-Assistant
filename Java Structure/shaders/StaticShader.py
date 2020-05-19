import ShaderProgram
import entities.Light

class StaticShader(ShaderProgram):
    MAX_LIGHTS = 4

    def __index__(self, vertexFile, fragmentFile):
        super().__init__(vertexFile, fragmentFile)
        self.location_lightColour = []
        self.location_lightPosition = []
        self.location_attenuation = []

    def bindAttributes(self):
        super().bindAttribute(0, "position")
        super().bindAttribute(1, "textureCoords")
        super().bindAttribute(2, "normal")


    def getAllUniformLocations(self):
        self.location_transformationMatrix = super().getUniformLocation("transformationMatrix")
        self.location_projectionMatrix = super().getUniformLocation("projectionMatrix")
        self.location_viewMatrix = super().getUniformLocation("viewMatrix")
        self.location_shineDamper = super().getUniformLocation("shineDamper")
        self.location_reflectivity = super().getUniformLocation("reflectivity")
        self.location_useFakeLighting = super().getUniformLocation("useFakeLighting")
        self.location_numberOfRows = super().getUniformLocation("numberOfRows")
        self.location_offset = super().getUniformLocation("offset")

        for i in range(self.MAX_LIGHTS):
            self.location_lightPosition[i] = super.getUniformLocation("lightPosition[{}]".format(i))
            self.location_lightColour[i] = super.getUniformLocation("lightColour[{}]".format(i))
            self.location_attenuation[i] = super.getUniformLocation("attenuation[{}]".format(i))

    def loadNumberOfRows(self, numberOfRows):
        super.loadFloat(self.location_numberOfRows, numberOfRows)

    def loadOffset(self, x, y):
        super.load2DVector(self.location_offset, [x,y])

    def loadFakeLightingVariable(self, useFake):
        super.loadBoolean(self.location_useFakeLighting, useFake)

    def loadShineVariables(self, damper, reflectivity):
        super.loadFloat(self.location_shineDamper, damper)
        super.loadFloat(self.location_reflectivity, reflectivity)

    def loadTransformationMatrix(self, matrix):
        super.loadMatrix(self.location_transformationMatrix, matrix)

    def loadLights(self, lights):
        for i in range(self.MAX_LIGHTS):
            if i < len(lights):
                super.loadVector(self.location_lightPosition[i], lights.get(i).getPosition())
                super.loadVector(self.location_lightColour[i], lights.get(i).getColour())
                super.loadVector(self.location_attenuation[i], lights.get(i).getAttenuation())
            else:
                super.loadVector(self.location_lightPosition[i], [0.0, 0.0, 0.0])
                super.loadVector(self.location_lightColour[i], [0.0, 0.0, 0.0])
                super.loadVector(self.location_attenuation[i], [1.0, 0.0, 0.0])

    def loadViewMatrix(self, camera):
        viewMatrix = Math.createViewMatrix(camera)
        super.loadMatrix(self.location_viewMatrix, viewMatrix)

    def loadProjectionMatrix(self, projection):
        super.loadMatrix(self.location_projectionMatrix, projection)