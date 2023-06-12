from .organism import Organism


class Animal(Organism):
    def __init__(self, positionX, positionY, strength, innitiative):
        super(Animal, self).__init__(positionX, positionY, strength, innitiative)
    def reproduceMessage(self):
        return "was born"
    def action(self):
        self.basicMovementHandle()
        self.basicCollisionHandle()
    
    def collision(self):
        from .functions import CollisionAction
        output = CollisionAction()
        output.realStrength = self.strength()
        return output
    
    def basicMovementHandle(self):
        from .functions import Vector2
        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())
        directions = self.world().directions()
        #Randomize a direction;
        direction = directions[random.randint(0, len(directions)-1)] 

        coordinate = Vector2(0, 0)
        coordinate.x = self._positionX + direction.x
        coordinate.y = self._positionY + direction.y
        
        #Find a valid cell
        while(not self.world().isInBounds(coordinate)):
            direction = directions[random.randint(0, len(directions)-1)] 
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y

        self._move.x = coordinate.x
        self._move.y = coordinate.y
    
    def basicCollisionHandle(self):
        thisOrganism = self._world.board()[self._positionX][self._positionY]
        otherOrganism = self._world.board()[self._move.x][self._move.y]

        if(otherOrganism == None):
            thisOrganism.moveOrganism(self._move.x, self._move.y)
            return
       
        if(self.reproduceAnimal(otherOrganism)):
            return
 

        thisCollision = self.collision()
        otherCollision = otherOrganism.collision()
        
        if(thisCollision.escaped == True):
            return


        if(otherCollision.escaped == True):
            moveOrganism(self._move.x, self._move.y)
            return
        
        thisOrganism.killIfStronger(otherOrganism, thisCollision, otherCollision)
    
    reproduce_chance = 25

    def reproduceAnimal(self, otherOrganism):
        if(not type(self) == type(otherOrganism)):
            return False

        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        if(random.randint(0, 100) > self.reproduce_chance):
            return True

        directions = self._world.directions()
        directionsDiagonal = self._world.directionsDiagonal()
        from .functions import Vector2
        coordinate = Vector2(0, 0)
        
        emptyCellsThis = []
        emptyCellsOther = []

        #Get all empty cells around a first parent
        for direction in directions + directionsDiagonal:
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            targetOrganism = self._world.board()[coordinate.x][coordinate.y]
            if(targetOrganism == None):
                emptyCellsThis.append(Vector2(coordinate.x, coordinate.y))

        #Get all empty cells around a second parent
        for direction in directions + directionsDiagonal:
            coordinate.x = otherOrganism.positionX() + direction.x
            coordinate.y = otherOrganism.positionY() + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            targetOrganism = self._world.board()[coordinate.x][coordinate.y]
            if(targetOrganism == None):
                emptyCellsOther.append(Vector2(coordinate.x, coordinate.y))
        if(len(emptyCellsThis) == 0 or len(emptyCellsOther) == 0):
            return True
        
        #print(len(emptyCellsThis))
        #print(len(emptyCellsOther))
        finalCells = []

        for thisCell in emptyCellsThis:
            for otherCell in emptyCellsOther:
                #print(str(otherCell.x) + ", " + str(otherCell.y) +  " = " + str(thisCell.x) + ", " + str(thisCell.y) + " ? " + str(otherCell == thisCell))
                if(otherCell == thisCell):
                    finalCells.append(Vector2(thisCell.x, thisCell.y))

        #print(len(finalCells))

        if(len(finalCells) == 0):
            return True
        
        direction = finalCells[random.randint(0, len(finalCells)-1)]

        self.reproduce(direction.x, direction.y)

        # Message message = new Message();
        # message.addToList(getClass().getSimpleName()); 
        # message.addToList(getBornMessage());

        # world.manager().pushMessage(message);
        #TODO
        return True
