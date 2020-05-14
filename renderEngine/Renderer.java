class Renderer:
    def __init__(self):

    def prepare(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def render(modelData):
        glBindVertexArray(modelData.getVaoID())
        glEnableVertexAttribArray(0)    # Data stored in vertex attribute '0' as coded in ModelData
        glDrawArrays(GL_TRIANGLES, 0, modelData.getVertexCount())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
