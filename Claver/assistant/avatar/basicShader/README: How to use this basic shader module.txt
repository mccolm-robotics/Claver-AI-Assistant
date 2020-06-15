Add the following to the initialize function:
     self.basic = BasicTile(self.loader, (0, .2, 0))

Add the following to the __init__ function of the MasterRenderer class:
    self.__basicShader = BasicShader()
    shaderList.append(self.__basicShader)
    self.__basicRenderer = BasicRenderer(self.__basicShader, self.__projectionMatrix, self.__camera)

Add the following to the render function of the MasterRenderer class:
    self.__waterRenderer.render(self.water, clock)

Add this to the cleanUp() function of the MasterRenderer class:
    self.__basicShader.cleanUp()