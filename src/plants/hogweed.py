from .. import plant 

class Hogweed(plant.Plant):
    def __init__(self, positionX, positionY):
            super(Hogweed, self).__init__(positionX, positionY, 10)   
    def displayChar(self):
        return "H"
    def name(self):
        return "Hogweed"
        
    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        action.killAfterDefeat = True
        return action
    
    def action(self):
        from ..functions import Vector2
        directions = self._world.directions()

        coordinate = Vector2(0,0)
        for direction in directions:
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            target = self._world.board()[coordinate.x][coordinate.y]
            if(target != None):
                from ..plant import Plant
                if(Plant.__subclasscheck__(target.__class__)):
                    continue
                from ..functions import CollisionAction
                action = target.collision()
                
                if(action.isImmortal):
                    continue
                if(action.isImmuneToHogweed):
                    continue
                #TODO message
                target.die()
        
        self.basicGrowHandle()