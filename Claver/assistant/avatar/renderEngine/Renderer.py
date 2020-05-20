from Claver.assistant.avatar.models.RawModel import RawModel
from Claver.assistant.avatar.models.TexturedModel import TexturedModel
from OpenGL.GL import *


class Renderer:
    def __init__(self):
        pass

    def prepare(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)                    # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT)  # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER

    def render(self, texturedModel):
        model = texturedModel.getRawModel()
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texturedModel.getTexture().getID())
        glDrawArrays(GL_TRIANGLE_FAN, 0, model.getVertexCount())
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindVertexArray(0)
