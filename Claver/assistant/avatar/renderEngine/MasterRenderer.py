from OpenGL.GL import *

from Claver.assistant.avatar.shaders.StaticShader import StaticShader
from Claver.assistant.avatar.renderEngine.EntityRenderer import EntityRenderer
from Claver.assistant.avatar.shaders.TerrainShader import TerrainShader
from Claver.assistant.avatar.renderEngine.TerrainRenderer import TerrainRenderer
from Claver.assistant.avatar.entities.Entity import Entity
from Claver.assistant.avatar.entities.Light import  Light
from Claver.assistant.avatar.entities.Camera import Camera
from Claver.assistant.avatar.toolbox.Math import createProjectionMatrix

class MasterRenderer:

    __RED = 0.5
    __GREEN = 0.5
    __BLUE = 0.5

    def __init__(self, window, keyboardEvents, player):
        glEnable(GL_DEPTH_TEST) # Enable depth testing to ensure pixels closer to the viewer appear closest
        glDepthFunc(GL_LESS)    # Set the type of calculation used by the depth buffer
        MasterRenderer.enableCulling()
        shaderList = []
        self.__shader = StaticShader()
        shaderList.append(self.__shader)
        self.__terrainShader = TerrainShader()
        shaderList.append(self.__terrainShader)
        self.__camera = Camera(window, keyboardEvents, shaderList, player)
        self.__projectionMatrix = self.__camera.getProjectionMatrix()
        self.__renderer = EntityRenderer(self.__shader, self.__projectionMatrix)
        self.__entityDict = {}
        # Added for terrains
        self.__terrains = []
        self.__terrainRenderer = TerrainRenderer(self.__terrainShader, self.__projectionMatrix)

    @staticmethod
    def enableCulling():
        glEnable(GL_CULL_FACE)  # Enable face culling
        glCullFace(GL_BACK)     # Discard the back faces of polygons (determined by the vertex winding order)

    @staticmethod
    def disableCulling():
        glDisable(GL_CULL_FACE)

    def prepare(self, time):
        self.__applicationTime = time
        glClearColor(self.__RED, self.__GREEN, self.__BLUE, 0.0)  # Set the background colour for the window -> Black
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the window background colour to black by resetting the COLOR_BUFFER and clear the DEPTH_BUFFER

    def processMovement(self, timeDelta):
        self.__camera.move(timeDelta)

    def render(self, sun, clock):
        self.prepare(clock)
        self.__shader.start()
        self.__shader.loadSkyColour(self.__RED, self.__GREEN, self.__BLUE)
        self.__shader.loadLight(sun)
        self.__shader.loadViewMatrix(self.__camera)
        self.__renderer.render(self.__entityDict, clock)
        self.__shader.stop()
        self.__terrainShader.start()
        self.__terrainShader.loadSkyColour(self.__RED, self.__GREEN, self.__BLUE)
        self.__terrainShader.loadLight(sun)
        self.__terrainShader.loadViewMatrix(self.__camera)
        self.__terrainRenderer.render(self.__terrains, clock)
        self.__terrainShader.stop()
        self.__terrains.clear()
        self.__entityDict.clear()

    def processTerrain(self, terrain):
        self.__terrains.append(terrain)

    def processEntity(self, entity):
        entityModel = entity.getModel()
        if entityModel in self.__entityDict:
            self.__entityDict[entityModel].append(entity)
        else:
            self.__entityDict[entityModel] = [entity]

    def cleanUp(self):
        self.__shader.cleanUp()
        self.__terrainShader.cleanUp()

    def windowResized(self, width, height):
        self.__camera.recalculateProjectionMatrix(width, height)

    def getCamera(self):
        return self.__camera