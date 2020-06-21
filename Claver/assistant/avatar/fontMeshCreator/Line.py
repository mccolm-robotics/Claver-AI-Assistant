from Claver.assistant.avatar.fontMeshCreator.Word import Word

class Line:
    def __init__(self, spaceWidth, fontSize, maxLength):
        self.__spaceSize = spaceWidth * fontSize
        self.__maxLength = maxLength
        self.__words = []
        self.__currentLineLength = 0

    def attemptToAddWord(self, word):
        additionalLength = word.getWordWidth()
        additionalLength += self.__spaceSize if self.__words else 0
        if self.__currentLineLength + additionalLength <= self.__maxLength:
            self.__words.append(word)
            self.__currentLineLength += additionalLength
            return True
        else:
            return False

    def getMaxLength(self):
        return self.__maxLength

    def getLineLength(self):
        return self.__currentLineLength

    def getWords(self):
        return self.__words