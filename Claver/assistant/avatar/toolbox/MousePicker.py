import pyrr
from pyrr import Vector3, Vector4, Matrix44
from Claver.assistant.avatar.toolbox.Math import createViewMatrix

class MousePicker:
    def __init__(self, camera, projectionMatrix, inputEvents, window):
        self.__currentRay = Vector3((0,0,0))
        self.__inputEvents = inputEvents
        self.__projectionMatrix = projectionMatrix
        self.__camera = camera
        self.__viewMatrix = createViewMatrix(camera)
        self.__windowWidth = window.width
        self.__windowHeight = window.height

    def getCurrentRay(self):
        return self.__currentRay

    def update(self):
        self.__viewMatrix = self.__camera.getViewMatrix()
        self.__currentRay = self.__calculateMouseRay()

    def __calculateMouseRay(self):
        # Position of mouse in viewport space
        mouseX, mouseY = self.__inputEvents.getCursorPosition()
        normalizedCoords = self.getNormalizedDeviceCoords(mouseX, mouseY)
        clipCoords = Vector4((normalizedCoords[0], normalizedCoords[1], -1, 1))
        eyeCoords = self.toEyeCoords(clipCoords)
        worldRay = self.toWorldCoords(eyeCoords)
        return worldRay

    def toWorldCoords(self, eyeCoords):
        invertedView = pyrr.matrix44.inverse(self.__viewMatrix)
        rayWorld = pyrr.matrix44.apply_to_vector(invertedView, eyeCoords)
        mouseRay = Vector3((rayWorld.x, rayWorld.y, rayWorld.z))
        mouseRayNormalised = pyrr.vector3.normalize(mouseRay)
        return mouseRayNormalised

    def toEyeCoords(self, clipCoords):
        invertedProjection = pyrr.matrix44.inverse(self.__projectionMatrix)
        eyeCoords = pyrr.matrix44.apply_to_vector(invertedProjection, clipCoords)
        return Vector4((eyeCoords[0], eyeCoords[1], -1, 0))

    def getNormalizedDeviceCoords(self, mouseX, mouseY):
        # Convert from screen (mouse) coordinates to the OpenGL coordinate system --> mouse in normalized device space
        x = (2 * mouseX) / self.__windowWidth - 1
        y = (2 * mouseY) / self.__windowHeight -1
        return (x, -y)


