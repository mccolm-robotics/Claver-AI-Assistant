import fontMeshCreator.FontType
import fontMeshCreator.GUIText
import renderEngine.Loader

class TextMaster:
    loader = None
    texts = {}
    renderer = None

    @classmethod
    def init(cls,theLoader):
        cls.renderer = FontRenderer()
