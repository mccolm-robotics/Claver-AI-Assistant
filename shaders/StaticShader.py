import ShaderProgram

class StaticShader(ShaderProgram):
    def __index__(self, vertexFile, fragmentFile):
        super().__init__(vertexFile, fragmentFile)

    def bindAttributes(self):
        super().bindAttribute(0, "position")