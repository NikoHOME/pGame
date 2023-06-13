from .. import animal 

class BfsData:
    def __init__(self, x, y, distance):
        self.x = x
        self.y = y
        self.distance = distance

class CyberSheep(animal.Animal):
    def __init__(self, positionX, positionY):
        super(CyberSheep, self).__init__(positionX, positionY, 11, 4)
        self._hogweed = None
    def displayChar(self):
        return "C"
    def name(self):
        return "Cyber Sheep"
    
    def action(self):
        from ..plants.hogweed import Hogweed
        from ..functions import Vector2
        visited = [[ False for y in range(self._world.height())] for x in range(self._world.width())]
        found = []
        queue = []
        queue.append(BfsData(self._positionX, self._positionY, 0))
        visited[self._positionX][self._positionY] = True
        directions = self._world.directions()

        while queue:        
            nextNode = queue.pop(0) 
            #print(str(nextNode.x) + " " + str(nextNode.y) + " " +str(nextNode.distance))
            coordinate = Vector2(0,0)
            
            for direction in directions:
                coordinate.x = nextNode.x + direction.x
                coordinate.y = nextNode.y + direction.y
                if(not self._world.isInBounds(coordinate)):
                    continue
                if(not visited[coordinate.x][coordinate.y]):
                    visited[coordinate.x][coordinate.y] = True
                    queue.append(BfsData(coordinate.x, coordinate.y, nextNode.distance+1))
                    target = self._world.board()[coordinate.x][coordinate.y]
                    if(Hogweed.__subclasscheck__(target.__class__)):
                        found.append(BfsData(coordinate.x, coordinate.y, nextNode.distance+1))

        if(len(found) == 0):
            self.basicMovementHandle()
            self.basicCollisionHandle()
            return

        closest = found[0]
        for hogweed in found:
            if(hogweed.distance < closest.distance):
                closest = hogweed
        self._hogweed = self._world.board()[closest.x][closest.y]

        differenceX = self.positionX() - self._hogweed.positionX()
        differenceY = self.positionY() - self._hogweed.positionY()

        
        simpleX = 0
        simpleY = 0
        if(differenceX < 0):
            simpleX = 1
        elif(differenceX > 0):
            simpleX = -1

        if(differenceY < 0):
            simpleY = 1
        elif(differenceY > 0):
            simpleY = -1

        if(simpleX == 0 or simpleY == 0):
            self._move.x = self.positionX() + simpleX
            self._move.y = self.positionY() + simpleY
            self._hogweed = None
            self.basicCollisionHandle()
            return
        
        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        if(random.randint(0, 1) == 0):
            self._move.x = self.positionX() + simpleX
            self._move.y = self.positionY()
        else:
            self._move.x = self.positionX()
            self._move.y = self.positionY() + simpleY

        self._hogweed = None
        self.basicCollisionHandle()

    def collision(self):
        from ..functions import CollisionAction
        action = CollisionAction()
        action.realStrength = self._strength
        action.isImmuneToHogweed = True
        return action