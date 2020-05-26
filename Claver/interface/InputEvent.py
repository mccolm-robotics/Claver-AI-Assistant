class InputEvent:
    def __init__(self):
        self.__keysPressed = set()
        self.__cursor_position = (300,600)
        self.__device = None
        self.__starting_coordinate = None

    def registerKeyboardEvent(self, key):
        self.__keysPressed.add(key)

    def cancelKeyboardEvent(self, key):
        self.__keysPressed.discard(key)

    def isKeyDown(self, character):
        if ord(character) in self.__keysPressed:
            return True
        else:
            return False

    def setCursorPosition(self, position):
        self.__cursor_position = position

    def setStaringCoordinate(self, StPosition):
        self.__starting_coordinate = StPosition

    def getStartingCoordinate(self):
        return self.__starting_coordinate

    def setDevice(self, device):
        self.__device = device

    def getCursorPosition(self):
        return self.__cursor_position

    def getDevice(self):
        return self.__device