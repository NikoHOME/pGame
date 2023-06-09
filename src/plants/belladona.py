from .. import plant 

class Belladona(plant.Plant):
    def __init__(self, positionX, positionY):
            super(Belladona, self).__init__(positionX, positionY, 99)
    def displayChar(self):
        return "B"
    def name(self):
        return "Belladona"
    def displayColour(self):
        return (0, 20, 60, 255)
    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        action.killAfterDefeat = True
        return action