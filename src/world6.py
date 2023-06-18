from .world import World
from .functions import Vector2

class World6(World):
    def __init__(self, width, height, manager, populateFlag = True):
        
        super(World6, self).__init__(width, height, manager, populateFlag)

        self.isHex = True

        self._directions = []
        self._directions.append(Vector2(0, -1))
        self._directions.append(Vector2(0, 1))
        self._directions.append(Vector2(1, 0))
        self._directions.append(Vector2(-1, 0))
        self._directions.append(Vector2(1,-1))
        self._directions.append(Vector2(-1,1))

        self._directionsDiagonal = []
