import abc



class Organism(abc.ABC):
    def __init__(self, positionX, positionY, strength, innitiative):
            self._positionX = positionX
            self._positionY = positionY
            self._strength = strength
            self._innitiative = innitiative
            self._index = 0
            self._isDead = True
            self._world = None
            from .functions import Vector2
            self._move = Vector2(0,0)

    def positionX(self, newValue = None):
        if(newValue != None):
            self._positionX = newValue
        else:
            return self._positionX
    def positionY(self, newValue = None):
        if(newValue != None):
            self._positionY = newValue
        else:
            return self._positionY
    def strength(self, newValue = None):
        if(newValue != None):
            self._strength = newValue
        else:
            return self._strength
    def innitiative(self, newValue = None):
        if(newValue != None):
            self._innitiative = newValue
        else:
            return self._index
    def index(self, newValue = None):
        if(newValue != None):
            self._index = newValue
        else:
            return self._index
    def isDead(self, newValue = None):
        if(newValue != None):
            self._isDead = newValue
        else:
            return self._isDead
    def world(self, newValue = None):
        if(newValue != None):
            self._world = newValue
        else:
            return self._world
    def move(self, newValue = None):
        if(newValue != None):
            self._move = newValue
        else:
            return self._move

    @abc.abstractmethod
    def action(self):
        ...
    @abc.abstractmethod
    def collision(self):
        ...
    @abc.abstractmethod
    def displayChar(self):
        ...

    @abc.abstractmethod
    def name(self):
        ...

    @abc.abstractmethod
    def reproduceMessage(self):
        ...
    def displayColour(self):
        return (255, 255, 255, 255)

    def killMessage(self):
        return "killed"

    def moveOrganism(self, x, y):
        self.world().board()[x][y] = self
        self.world().board()[self._positionX][self._positionY] = None
        self._positionX = x
        self._positionY = y
    def die(self):
        self._isDead = True
        self.world().board()[self._positionX][self._positionY] = None
        self.world().update()

    def reproduce(self, x, y):
        newOrganism = self.__class__(x, y)
        self.world().manager().addMessage(newOrganism.name() + " " + newOrganism.reproduceMessage())
        self._world.add_organism(newOrganism)

    def pickRandomCell(self):
        from .functions import Vector2
        import random
        from datetime import datetime
        random.seed(datetime.now().timestamp())

        directions = self.world().directions()
        direction = directions[random.randint(0, len(directions)-1)] 

        coordinate = Vector2(0, 0)
        coordinate.x = self._positionX + direction.x
        coordinate.y = self._positionY + direction.y
        
        #Find a valid cell
        while(not self.world().isInBounds(coordinate)):
            direction = directions[random.randint(0, len(directions)-1)] 
            coordinate.x = self._positionX + direction.x
            coordinate.y = self._positionY + direction.y
        
        return coordinate

        
    def setAction(self, action, thisCollision, otherCollision):


        if(thisCollision.hasTempAttackStrength):
            action.thisAttackerStrength = thisCollision.tempAttackStrength
        else:
            action.thisAttackerStrength = thisCollision.realStrength
        
        if(thisCollision.hasTempDefenceStrength):
            action.thisDefenderStrength = thisCollision.tempDefenceStrength
        else:
            action.thisDefenderStrength = thisCollision.realStrength


        if(otherCollision.hasTempAttackStrength):
            action.otherAttackerStrength = otherCollision.tempAttackStrength
        else:
            action.otherAttackerStrength = otherCollision.realStrength
        
        if(otherCollision.hasTempDefenceStrength):
            action.otherDefenderStrength = otherCollision.tempDefenceStrength
        else:
            action.otherDefenderStrength = otherCollision.realStrength

        #Immunity
        if(thisCollision.isImmuneToHogweed and otherCollision.isHogweed):
            action.thisDefenderStrength = float('inf')
            thisCollision.isImmortal = True

    def killIfStronger(self, inputOrganism, thisCollision, otherCollision):

        thisOrganism = self._world.board()[self._positionX][self._positionY]
        otherOrganism = self._world.board()[inputOrganism.positionX()][inputOrganism.positionY()]

        from .functions import AttackAction
        action = AttackAction()

        self.setAction(action, thisCollision, otherCollision)

        if(action.thisAttackerStrength >= action.otherDefenderStrength):
    
            if(otherCollision.givesStrength):
                self.strength(self._strength + otherCollision.givenStrength)

            if(otherCollision.killAfterDefeat and not thisCollision.isImmortal):
                
                self.world().manager().addMessage(thisOrganism.name() + " " + thisOrganism.killMessage()  + " " + otherOrganism.name()  )
                self.world().manager().addMessage(otherOrganism.name() + " " + otherOrganism.killMessage()  + " " + thisOrganism.name()  )

                thisOrganism.die()
                otherOrganism.die()
                return

            self.world().manager().addMessage(thisOrganism.name() + " " + thisOrganism.killMessage()  + " " + otherOrganism.name()  )
            
            newPosX = otherOrganism.positionX()
            newPosY = otherOrganism.positionY()
            otherOrganism.die()

            self.moveOrganism(newPosX, newPosY)

        if(thisCollision.escapeAfterFailedAttack and action.thisAttackerStrength < action.otherDefenderStrength):

            from .functions import Vector2
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
                self.world().manager().addMessage(thisOrganism.name() + " escaped from " + otherOrganism.name()  )
                return

            import random
            from datetime import datetime
            random.seed(datetime.now().timestamp())

            self.world().manager().addMessage(thisOrganism.name() + " escaped from " + otherOrganism.name()  )
            self._move = safeDirections[random.randint(0, len(safeDirections) - 1)]     
            self.moveOrganism(self._move.x, self._move.y)
            
            return
            
        if(action.otherAttackerStrength > action.thisDefenderStrength):

            if(thisCollision.givesStrength):
                otherOrganism.strength(otherOrganism.strength() + thisCollision.givenStrength)


            self.world().manager().addMessage(otherOrganism.name() + " " + otherOrganism.killMessage()  + " " + thisOrganism.name()  )
            
            thisOrganism.die()
        
    
