from .. import animal 

class Player(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Player, self).__init__(positionX, positionY, 5, 4)
    def displayChar(self):
        return "@"
    def name(self):
        return "Player"
    
    def displayColour(self):
        return (255, 60, 60, 255)

    def action(self):
        self.basicCollisionHandle()

    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        if(self.world().playerAbilityOn()):
            action.isImmortal = True
            action.hasTempDefenceStrength = True
            import sys
            action.tempDefenceStrength = float('inf')
            action.escapeAfterFailedAttack = True
        return action