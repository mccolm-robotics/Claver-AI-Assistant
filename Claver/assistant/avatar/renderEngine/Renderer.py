from Claver.assistant.avatar.models.RawModel import *
from OpenGL.GL import *


class Renderer:
    def __init__(self):
        pass

    def prepare(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)                    # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT)  # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER

    def render(self, model):
        glBindVertexArray(model.getVaoID())
        glEnableVertexAttribArray(0)
        glDrawArrays(GL_TRIANGLES, 0, model.getVertexCount())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
