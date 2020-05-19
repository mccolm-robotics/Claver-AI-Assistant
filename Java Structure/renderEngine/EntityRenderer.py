import models.ModelData

class EntityRenderer:
    # * (StaticShader) shader
    def __init__(self, shader, projectionMatrix):
        self.shader = shader
        self.shader.start()
        self.shader.loadProjectionMatrix(projectionMatrix)
        self.shader.stop()

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
        self.shader.loadNumberOfRows(texture.getNumberOfRows())
        if(texture.isHasTransparency()):
            MasterRenderer.disableCulling()
        self.shader.loadFakeLightingVariable(texture.isUseFakeLighting())
        self.shader.loadShineVariables(texture.getShineDamper(), texture.getReflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturedModel.getTexture().getID())

    def unbindTexturedModel(self):
        MasterRenderer.enableCulling()
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def prepareInstance(self, entity):
        transformationMatrix = Math.createTransformationMatrix(entity.getPosition(), entity.getRotX(), entity.getRotY(),
                                                               entity.getRotZ(), entity.getScale())
        self.shader.loadTransformationMatrix(transformationMatrix)
        self.shader.loadOffset(entity.getTextureXOffset(), entity.getTextureYOffset())
