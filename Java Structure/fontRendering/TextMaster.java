class TextMaster:

    private static Map<FontType, List<GUIText>> texts = new HashMap<FontType, List<GUIText>>()

    def __init__(self, Loader theLoader):
        self.renderer = FontRenderer()
        self.loader = theLoader

    def render(self):
        renderer.render(texts)

    def loadText(self, text):
        font = text.getFont()   # (FontType) font
        data = font.loadText(text)  # (TextMeshData) data
        int vao = loader.loadToVAO(data.getVertexPositions(), data.getTextureCoords())
        text.setMeshInfo(vao, data.getVertexCount())
        textBatch = self.texts.get(font)
        if(textBatch == None):
            textBatch = []
            self.texts.append(font:textBatch)
        textBatch.append(text)

    def removeText(self, GUIText text):
        textBatch = self.texts.get(text.getFont())
        textBatch.remove(text)
        if(textBatch.isEmpty()):
            texts.remove(text.getFont())

    def cleanUp(self):
        self.renderer.cleanUp()



So... calling this font:
    Loader loader = new Loader();
    TextMaster.init(loader);
    FontType font = new FontType(loader.loadTexture("verdana"), new File("verdana.fnt"));
    # Parameters (
        text to render,
        font size,
        font,
        the position,
        line length -> 1.0 = width of screen,
        whether text is centered)
    GUIText text = new GUIText ("This is a test text!", 1, font, new Vector2f(0,0), 1.0, true);
    text.setColour(1,0,0);