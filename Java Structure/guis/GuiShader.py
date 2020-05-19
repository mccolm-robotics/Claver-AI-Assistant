import shaders.ShaderProgram

class GuiShader(ShaderProgram):
    def __init__(self):
        VERTEX_FILE = "src/guis/guiVertexShader.txt"
        FRAGMENT_FILE = "src/guis/guiFragmentShader.txt"
        super().__init__(VERTEX_FILE, FRAGMENT_FILE)

    def loadTransformation(self, matrix):
        super.loadMatrix(self.location_transformationMatrix, matrix)

    def getAllUniformLocations(self):
        self.location_transformationMatrix = super.getUniformLocation("transformationMatrix")

    def bindAttributes(self):
        super.bindAttrib(0, "position")