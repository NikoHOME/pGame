from .. import animal 

class Player(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Player, self).__init__(positionX, positionY, 5, 4)
    def displayChar(self):
        return "P"
    def name(self):
        return "Player"

    def action(self):
        self.basicCollisionHandle()

    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        if(self.world().playerAbilityOn()):
            action.isImmortal = True
        return action