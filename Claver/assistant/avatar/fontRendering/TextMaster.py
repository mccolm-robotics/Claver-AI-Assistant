from Claver.assistant.avatar.fontRendering.FontRenderer import FontRenderer
from Claver.assistant.avatar.fontMeshCreator.FontType import FontType
from Claver.assistant.avatar.fontMeshCreator.TextMeshData import TextMeshData

class TextMaster:

    __loader = None
    __texts = {}
    __renderer = None

    @staticmethod
    def init(theLoader):
        TextMaster.__renderer = FontRenderer()
        TextMaster.__loader = theLoader

    @staticmethod
    def render():
        TextMaster.__renderer.render(TextMaster.__texts)

    @staticmethod
    def loadText(text):
        font = text.getFont()
        data = font.loadText(text)
        vao = TextMaster.__loader.loadQuadToVAO(data.getVertexPositions(), data.getTextureCoords())
        text.setMeshInfo(vao, data.getVertexCount())
        if font in TextMaster.__texts:
            textBatch = TextMaster.__texts[font]
        else:
            textBatch = []
            TextMaster.__texts[font] = textBatch
        textBatch.append(text)      # Pass-by-reference means text is added to the dictionary

    @staticmethod
    def removeText(text):
        if text.getFont() in TextMaster.__texts:
            textBatch = TextMaster.__texts[text.getFont()]
            textBatch.remove(text)
            if not textBatch:
                del TextMaster.__texts[text.getFont()]
                # Also delete text's VAO and related VBOs?

    @staticmethod
    def cleanUp():
        TextMaster.__renderer.cleanUp()
