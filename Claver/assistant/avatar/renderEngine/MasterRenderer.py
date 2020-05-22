from Claver.assistant.avatar.shaders.StaticShader import StaticShader
from Claver.assistant.avatar.renderEngine.Renderer import Renderer
from Claver.assistant.avatar.entities.Entity import Entity
from Claver.assistant.avatar.entities.Light import  Light
from Claver.assistant.avatar.entities.Camera import Camera

class MasterRenderer:
    def __init__(self):
        self.__shader = StaticShader()
        self.__renderer = Renderer(self.__shader)
        self.__entityDict = {}

    def render(self, sun, camera, clock):
        self.__renderer.prepare(clock)
        self.__shader.start()
        self.__shader.loadLight(sun)
        self.__shader.loadViewMatrix(camera)
        self.__renderer.render(self.__entityDict)
        self.__shader.stop()
        self.__entityDict.clear()

    def processEntity(self, entity):
        entityModel = entity.getModel()
        if entityModel in self.__entityDict[entityModel]:
            self.__entityDict[entityModel].append(entity)
        else:
            self.__entityDict[entityModel] = [entity]


    def cleanUp(self):
        self.__shader.cleanUp()