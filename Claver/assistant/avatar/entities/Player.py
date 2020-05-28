from Claver.assistant.avatar.entities.Entity import Entity

class Player(Entity):
    __RUN_SPEED = 20        # units / sec
    __TURN_SPEED = 160      # deg / sec

    def __init__(self, model, position, rotX, rotY, rotZ, scale):
        super().__init__(model, position, rotX, rotY, rotZ, scale)

    def move(self):
