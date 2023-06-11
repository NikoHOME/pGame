from . import organism


class Plant(organism.Organism):

    

    def __init__(self, positionX, positionY, strength):
            super(Plant, self).__init__(positionX, positionY, strength, 0)
    def action(self):
        self.basicGrowHandle()
    def collision(self):
        from .functions import CollisionAction
        output = CollisionAction()
        output.realStrength = self.strength()
        return output
    
    grow_chance = 1
    
    def basicGrowHandle(self):

        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        if(random.randint(0, 100) > self.grow_chance):
            return False

        directions = self._world.directions()
        emptyCells = []
        from .functions import Vector2
        coordinate = Vector2(0, 0)
        #Find emtpy cells around a plant
        for direction in directions:
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
            if(not self._world.isInBounds(coordinate)):
                continue
            targetOrganism = self._world.board()[coordinate.x][coordinate.y]
            if(targetOrganism == None):
                emptyCells.append(Vector2(coordinate.x, coordinate.y))

        if(len(emptyCells) == 0):
            return True
        print(f"{len(emptyCells)} {len(directions)} {self.__class__}")

            
        direction = emptyCells[random.randint(0, len(emptyCells)-1)]

        self.reproduce(direction.x, direction.y)
        
        # Message message = new Message();
        # message.addToList(getClass().getSimpleName()); 
        # message.addToList(getBornMessage());

        # world.manager().pushMessage(message);
        #TODO

        return True