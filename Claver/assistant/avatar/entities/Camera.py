import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import pyrr
from math import sin, cos, radians
from pyrr import Vector3
from Claver.assistant.avatar.toolbox.Math import createViewMatrix, createProjectionMatrix

class Camera:
    __MOVEMENT_SPEED = 2.5
    __SENSITIVITY = 0.1
    __ZOOM_SENSITIVITY = 0.5
    __ZOOM_NEAR_LIMIT = 3
    __ZOOM_FAR_LIMIT = 10
    __FOV_LIMIT = 70
    __NEAR_PLANE = 0.1
    __FAR_PLANE = 1000

    def __init__(self, window, inputEvents, shaderList, player):
        self.__position = Vector3((0.0, 4.0, 4.0))
        self.__front = Vector3((0.0, 0.0, -1.0))
        self.__up = Vector3((0.0, 1.0, 0.0))
        self.__FOV = self.__FOV_LIMIT
        self.__width = window.width
        self.__height = window.height
        self.__inputEvents = inputEvents
        self.__shaderList = shaderList
        self.__pitch = 20             # Rotation around X axis: look up and down
        self.__yaw = 0           # Rotation around Y axis: look left and right. yaw is initalized to -90 since a yaw of 0.0 results in a direction vector pointing to the right
        self.__distanceFromPlayer = 5
        self.__angleAroundPlayer = 0
        self.__viewMatrix = None
        self.__projectionMatrix = None
        self.__previousMouseMovement = False
        self.__lastCursorPosition = None
        self.__startingCoordinate = None
        self.__screen = Gdk.Screen.get_default()
        self.initialized = False
        self.__setWarp = False
        self.__warpCounter = 0
        self.__player = player
        self.__playerRunSpeed = player.getRunSpeed()
        self.__updatePlayerYaw = False

    def __updateViewMatrix(self):
        self.__viewMatrix = createViewMatrix(self)

    def getViewMatrix(self):
        if self.__viewMatrix is None:
            self.__updateViewMatrix()
        return self.__viewMatrix

    def __updateProjectionMatrix(self):
        self.__projectionMatrix = createProjectionMatrix(self.__FOV, self.__width, self.__height, self.__NEAR_PLANE, self.__FAR_PLANE)

    def __loadProjectionMatrixToShader(self):
        for shader in self.__shaderList:
            shader.start()
            shader.loadProjectionMatrix(self.__projectionMatrix)
            shader.stop()

    def getProjectionMatrix(self):
        if self.__projectionMatrix is None:
            self.__updateProjectionMatrix()
        return self.__projectionMatrix

    def recalculateProjectionMatrix(self, width, height):
        self.__width = width
        self.__height = height
        self.__updateProjectionMatrix()
        self.__loadProjectionMatrixToShader()

    def setLastMovePosition(self, position):
        self.__lastCursorPosition = position

    def setStartingPosition(self, startPosition):
        self.__startingCoordinate = startPosition

    def activateWarp(self):
        self.__setWarp = True

    def deactivateWarp(self):
        self.__setWarp = False

    def move(self, delta):
        newCursorPosition = self.__inputEvents.getCursorPosition()
        if self.__inputEvents.getDevice() is not None:
            device = self.__inputEvents.getDevice()
            self.initialized = True

        if self.__lastCursorPosition is None:
            self.__lastCursorPosition = [300, 600]

        xoffset = newCursorPosition[0] - self.__lastCursorPosition[0]
        yoffset = self.__lastCursorPosition[1] - newCursorPosition[1]

        mouse_sensitivity = 0.1
        xoffset *= mouse_sensitivity
        yoffset *= mouse_sensitivity

        self.__yaw -= xoffset
        self.__pitch += yoffset

        # prevent screen from flipping when pitch is out of bounds
        if self.__pitch > 89.0:
            self.__pitch = 89.0
        if self.__pitch < -89.0:
            self.__pitch = -89.0

        if self.__yaw > 360:
            self.__yaw -= 360
        elif self.__yaw < 0:
            self.__yaw += 360

        distance = self.__playerRunSpeed * delta
        fwdVector = (self.__position.x - self.__player.getPosition().x, 0, self.__position.z - self.__player.getPosition().z)
        sideStepDirection = pyrr.vector3.normalize(pyrr.vector3.cross(fwdVector, self.__up))

        if self.__inputEvents.isKeyDown('a') is True or self.__inputEvents.isKeyDown('s') is True or self.__inputEvents.isKeyDown('d') is True or self.__inputEvents.isKeyDown('w') is True:
            if self.__inputEvents.isButtonDown(1) is True and self.__inputEvents.isButtonDown(3) is False:
                self.__player.move(delta, sideStepDirection)
            else:
                self.__player.move(delta, sideStepDirection, radians(self.__yaw))
        else:
            self.__player.move(delta, sideStepDirection)

        if self.__inputEvents.isKeyDown('a') is True and self.__inputEvents.isKeyDown('d') is False:
            self.__position += sideStepDirection * distance
        elif self.__inputEvents.isKeyDown('d') is True and self.__inputEvents.isKeyDown('a') is False:
            self.__position -= sideStepDirection * distance

        horizontalDistance = self.__distanceFromPlayer * cos(radians(self.__pitch))
        verticalDistance = self.__distanceFromPlayer * sin(radians(self.__pitch))
        self.__position.y = self.__player.getPosition().y + 2.5 + verticalDistance
        if self.__position.y < self.__player.getGroundHeight() + .5:
            self.__position.y = self.__player.getGroundHeight() + .5
        theta = self.__player.getRotY() + self.__yaw
        offsetX = horizontalDistance * sin(radians(theta))
        offsetZ = horizontalDistance * cos(radians(theta))
        self.__position.x = self.__player.getPosition().x - offsetX
        self.__position.z = self.__player.getPosition().z - offsetZ





        # front = Vector3((0.0, 0.0, 0.0))
        # front.x = cos(radians(self.__yaw)) * cos(radians(self.__pitch))
        # front.y = sin(radians(self.__pitch))
        # front.z = sin(radians(self.__yaw)) * cos(radians(self.__pitch))
        # self.__front = pyrr.vector3.normalize(front)





        self.__updateViewMatrix()

        if self.initialized is True and self.__setWarp is True:
            self.__warpCounter += 1
            if self.__warpCounter > 5:
                self.__lastCursorPosition = self.__startingCoordinate
                # warp is an extremely unoptimized function that introduces considerable lag. Call it every 6 frames to reduce overhead
                Gdk.Device.warp(device, self.__screen, self.__lastCursorPosition[0], self.__lastCursorPosition[1])
                self.__warpCounter = 0
            else:
                self.__lastCursorPosition = newCursorPosition

    def increaseFOV(self):
        self.__changeFOV(1)

    def decreaseFOV(self):
        self.__changeFOV(-1)

    def increaseZoom(self):
        self.calculateZoom(1)

    def decreaseZoom(self):
        self.calculateZoom(-1)

    def __changeFOV(self, flag):
        if 1.0 <= self.__FOV <= self.__FOV_LIMIT:
                self.__FOV -= flag * self.__ZOOM_SENSITIVITY
        if self.__FOV <= 1.0:
            self.__FOV = 1.0
        if self.__FOV >= self.__FOV_LIMIT:
            self.__FOV = self.__FOV_LIMIT
        self.__updateProjectionMatrix()
        self.__loadProjectionMatrixToShader()

    def getPosition(self):
        return self.__position

    def getPitch(self):
        return self.__pitch

    def getYaw(self):
        return self.__yaw

    def getFront(self):
        return self.__front

    def calculateZoom(self, amount):
        if self.__ZOOM_NEAR_LIMIT <= self.__distanceFromPlayer <= self.__ZOOM_FAR_LIMIT:
                self.__distanceFromPlayer += amount * self.__ZOOM_SENSITIVITY
        if self.__distanceFromPlayer <= self.__ZOOM_NEAR_LIMIT:
            self.__distanceFromPlayer = self.__ZOOM_NEAR_LIMIT
        if self.__distanceFromPlayer >= self.__ZOOM_FAR_LIMIT:
            self.__distanceFromPlayer = self.__ZOOM_FAR_LIMIT

    def getPlayer(self):
        return self.__player


# if __name__ == '__main__':
# # camera
# cameraPos = Vector3((0.0, 0.0, 3.0))
# cameraFront = Vector3((0.0, 0.0, -1.0))
# cameraUp = Vector3((0.0, 1.0, 0.0))
# yaw = -90.0     #yaw is initalized to -90 since a yaw of 0.0 results in a direction vector point to the right
# pitch = 0.0
# fov = 45.0
#
# # mouse state
# firstMouse = True
# lastX = 800 / 2
# lastY = 600 / 2
#
# # timing
# deltaTime = 0.0
# lastFrame = 0.0
#
# # mouse callbacks
# SetMouseCursorPositionCallback
# setMouseScrollCallback
#
# # y_offset is up and down of mouse scroll wheel (typical default behaviour)
# scroll_callback (x_offset, y_offset)
#     if fov >= 1.0 && fov <= 45.0:
#         fov -= y_offset
#     if fov <= 1.0:
#         fov = 1.0
#     if fov >= 45.0:
#         fov = 45.0
#
# # Capture the mouse
# SetInputMode(CURSOR, CURSOR_DISABLED)
#
# # Mouse movement callback
# mouse_callback(x_pos, y_pos):
#     if firstMouse == True:
#         lastX = x_pos
#         lastY = y_pos
#         firstMouse = False
#
#     xoffset = x_pos - lastX
#     yoffset = lastY - y_pos
#     lastX = x_pos
#     lastY = y_pos
#
#     mouse_sensitivity = 0.1
#     xoffset *= mouse_sensitivity
#     yoffset *= mouse_sensitivity
#
#     yaw += xoffset
#     pitch += yoffset
#
#     # prevent screen from flipping when pitch is out of bounds
#     if pitch > 89.0:
#         pitch = 89.0
#     if pitch < -89.0:
#         pitch = -89.0
#
#     front = Vector3((0.0, 0.0, 0.0))
#     front.x = cos(radians(yaw)) * cos(radians(pitch))
#     front.y = sin(radians(pitch))
#     front.z = sin(radians(yaw)) * cos(radians(pitch))
#     cameraFront = normalize(front)
#
# # camera / view transformation
# Matrix4 view = lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
#
# cameraSpeed = 2.5 * deltaTime
# if w:
#     cameraPos += cameraSpeed * cameraFront
# if s:
#     cameraPos -= cameraSpeed * cameraFront
# if a:
#     cameraPos -= normalize(cross(cameraFront, cameraUp)) * cameraSpeed
# if d:
#     cameraPos += normalize(cross(cameraFront, cameraUp)) * cameraSpeed
