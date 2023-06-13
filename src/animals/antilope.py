from .. import animal 

class Antilope(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Antilope, self).__init__(positionX, positionY, 4, 4)
    def displayChar(self):
        return "A"
    def name(self):
        return "Antilope"
    def displayColour(self):
        return (60, 30, 0, 255)
    def action(self):
        from ..functions import Vector2
        firstRandomCell = self.pickRandomCell()

        if(self._world.board()[firstRandomCell.x][firstRandomCell.y] != None):
            self._move = firstRandomCell
            self.basicCollisionHandle()
            return
        
        secondRandomCell = self.pickRandomCell()

        while(firstRandomCell == secondRandomCell):
            secondRandomCell = self.pickRandomCell()

        directionVectorFirst = Vector2(self.positionX() - firstRandomCell.x, self.positionY() - firstRandomCell.y)
        directionVectorSecond = Vector2(self.positionX() - secondRandomCell.x, self.positionY() - secondRandomCell.y)
        
        secondRandomCell = Vector2(firstRandomCell.x + directionVectorSecond.x, firstRandomCell.y + directionVectorSecond.y)


        if(firstRandomCell == secondRandomCell):
            finalMove = Vector2(firstRandomCell.x + directionVectorFirst.x, firstRandomCell.y + directionVectorFirst.y)

            if(self._world.isInBounds(finalMove)):
                self._move = finalMove
                self.basicCollisionHandle()
                return

            self._move = firstRandomCell
            self.basicCollisionHandle()
            return
        if(self._world.isInBounds(secondRandomCell)):
            self._move = secondRandomCell
            self.basicCollisionHandle()
            return

        self._move = firstRandomCell     
        self.basicCollisionHandle()

    def collision(self):
        from ..functions import Vector2
        from ..functions import CollisionAction

        action = CollisionAction()
        action.realStrength = self._strength

        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        if(random.randint(0, 1) == 1):
            return action
        

        directions = self._world.directions()
        safeDirections = []

        coordinate = Vector2(0,0)
        for direction in directions:
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            target = self._world.board()[coordinate.x][coordinate.y]
            if(target == None):
                safeDirections.append(Vector2(coordinate.x, coordinate.y))

        if(len(safeDirections) == 0):
            return action

        self._move = safeDirections[random.randint(0, len(safeDirections) - 1)]   

        self.moveOrganism(self._move.x, self._move.y)     
        self.world().manager().addMessage("Antilope escaped")
        action.escaped = True
        return action

    