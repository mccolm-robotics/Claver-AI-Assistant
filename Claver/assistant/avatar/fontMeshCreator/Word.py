from Claver.assistant.avatar.fontMeshCreator.Character import Character

class Word:
    def __init__(self, fontSize):
        self.__fontSize = fontSize
        self.__characters = []
        self.__width = 0

    # Adds a character to the end of the current word and increases the screen-space width of the word.
    def addCharacter(self, character):
        self.__characters.append(character)
        self.__width += character.getxAdvance() * self.__fontSize

    def getCharacters(self):
        return self.__characters

    def getWordWidth(self):
        return self.__width