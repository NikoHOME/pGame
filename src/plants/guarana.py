from .. import plant 

class Guarana(plant.Plant):
    def __init__(self, positionX, positionY):
            super(Guarana, self).__init__(positionX, positionY, 0)
    def displayChar(self):
        return "G"
    def name(self):
        return "Guarana"
    def displayColour(self):
        return (50, 5, 10, 255)
    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        action.givesStrength = True
        action.givenStrength = 3
        return action