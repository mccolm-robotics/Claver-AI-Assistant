class InputEvent:
    def __init__(self):
        self.__keysPressed = set()
        self.__cursor_position = [0,0]

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

    def getCursorPosition(self):
        return self.__cursor_position