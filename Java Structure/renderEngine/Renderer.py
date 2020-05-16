import models.ModelData

class Renderer:
    # * (StaticShader) shader
    def __init__(self, shader):
        self.FOV = 70
        self.NEAR_PLANE = 0.1
        self.FAR_PLANE = 1000
        self.shader = shader
        glEnable(GL_CULL_FACE)
        glCullFAce(GL_BACK)
        self.createProjectionMatrix()
        self.shader.start()
        self.shader.loadProjectionMatrix(self.projectionMatrix)
        self.shader.stop()

    def prepare(self):
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def render(self, entities_dict):
        for model_type in entities_dict:
            self.prepareTexturedModel(model_type)
            for entity in entities_dict[model_type]:
                self.prepareInstance(entity)
                glDrawArrays(GL_TRIANGLES, 0, entity.getModel().getVertexCount())
            self.unbindTexturedModel()

    def prepareTexturedModel(self, texturedModel):
        modelData = texturedModel.getModelData
        glBindVertexArray(modelData.getVaoID())
        glEnableVertexAttribArray(0)  # Data stored in vertex attribute '0' as coded in ModelData
        glEnableVertexAttribArray(1)  # Texture data
        glEnableVertexAttribArray(2)  # Normal data
        texture = texturedModel.getTexture()
        self.shader.loadShineVariables(texture.getShineDamper(), texture.getReflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturedModel.getTexture().getID())

    def unbindTexturedModel(self):
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def prepareInstance(self, entity):
        transformationMatrix = Math.createTransformationMatrix(entity.getPosition(), entity.getRotX(), entity.getRotY(),
                                                               entity.getRotZ(), entity.getScale())
        self.shader.loadTransformationMatrix(transformationMatrix)

    def createProjectionMatrix(self):
        aspectRatio =
        self.projectionMatrix =
