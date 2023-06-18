
from .world import World
from .functions import Vector2

class World4(World):
    def __init__(self, width, height, manager, populateFlag = True):
        
        super(World4, self).__init__(width, height, manager, populateFlag)

        self.isHex = False

        self._directions = []
        self._directions.append(Vector2(0, -1))
        self._directions.append(Vector2(0, 1))
        self._directions.append(Vector2(1, 0))
        self._directions.append(Vector2(-1, 0))

        self._directionsDiagonal = []
        self._directionsDiagonal.append(Vector2(-1, -1))
        self._directionsDiagonal.append(Vector2(-1, 1))
        self._directionsDiagonal.append(Vector2(1, -1))
        self._directionsDiagonal.append(Vector2(1, 1))