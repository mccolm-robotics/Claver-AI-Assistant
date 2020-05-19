class GuiRenderer:
    def __init__(self, loader):
        positions = [-1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0]
        self.quad = loader.loadGUIToVAO(positions, 2)
        self.shader = GuiShader()

    # * ([GUITexture]) guis
    def render(self, guis):
        self.shader.start()
        glBindVertexArray(self.quad.getVaoID())
        glEnableVertexAttribArray(0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        for guiTexture in guis:
            glActivateTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, guiTexture.getTexture())
            Matrix4f matrix = Math.createTransformationMatrix(guiTexture.getPosition(), guiTexture.getScale())
            self.shader.loadTransformation(matrix)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.quad.getVertexCount())
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.shader.stop()

    def cleanUp(self):
        self.shader.cleanUP()