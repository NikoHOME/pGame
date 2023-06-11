from .. import animal 

class Turtle(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Turtle, self).__init__(positionX, positionY, 2, 1)
    def displayChar(self):
        return "T"
    
    def action(self):
        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        if(random.randint(0, 3) != 0): # 25% chance of moving
            return
        
        self.basicMovementHandle()

        self.basicCollisionHandle()
    
    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        action.hasTempDefenceStrength = True
        action.tempDefenceStrength = 5
        return action