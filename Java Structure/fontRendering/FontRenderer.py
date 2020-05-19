import fontMeshCreator.GUIText;

class FontRenderer:

	def __init__(self):
		self.shader = FontShader()

	def cleanUp(self):
		self.shader.cleanUp()
	
	def prepare(self):
		pass

	# * (GUIText) text
	def renderText(self, text):
		pass
	
	def endRendering(self):
		pass