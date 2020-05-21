class KeyboardEvent:
    def __init__(self):
        self.__keysPressed = []

    def registerEvent(self, key):
        if key not in self.__keysPressed:
            self.__keysPressed.append(key)

    def cancelEvent(self, key):
        if key in self.__keysPressed:
            self.__keysPressed.remove(key)

    def isKeyDown(self, character):
        if ord(character) in self.__keysPressed:
            return True
        else:
            return False