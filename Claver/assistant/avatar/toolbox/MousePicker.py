from pyrr import Vector3, Matrix44
from Claver.assistant.avatar.toolbox.Math import createViewMatrix

class MousePicker:
    def __init__(self, camera, projectionMatrix, inputEvents):
        self.__currentRay = Vector3((0,0,0))
        self.__inputEvents = inputEvents
        self.__projectionMatrix = projectionMatrix
        self.__camera = camera
        self.__viewMatrix = createViewMatrix(camera)

    def getCurrentRay(self):
        return self.__currentRay

    def update(self):
        self.__viewMatrix = self.__camera.getViewMatrix()
        self.__currentRay = self.__calculateMouseRay()

    def __calculateMouseRay(self):
        # Position of mouse in viewport space
        mouseX, mouseY = self.__inputEvents.getCursorPosition()
        # Convert from screen coordinates to the OpenGL coordinate system --> mouse in normalized device space


