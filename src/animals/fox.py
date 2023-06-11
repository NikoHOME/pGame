from .. import animal 

class Fox(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Fox, self).__init__(positionX, positionY, 3, 7)

    def displayChar(self):
        return "F"

    def action(self):
        from ..functions import Vector2
        directions = self._world.directions()
        safeDirections = []

        coordinate = Vector2(0,0)
        for direction in directions:
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            target = self._world.board()[coordinate.x][coordinate.y]
            if(target == None or target.strength() <= self._strength or isinstance(self, target.__class__)):
                safeDirections.append(Vector2(coordinate.x, coordinate.y))

        if(len(safeDirections) == 0):
            return

        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        self._move = safeDirections[random.randint(0, len(safeDirections) - 1)]        
        
        self.basicCollisionHandle()