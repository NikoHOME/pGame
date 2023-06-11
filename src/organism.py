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

    def positionX(self):
        return self._positionX
    def positionY(self):
        return self._positionY
    def strength(self, newValue = None):
        if(newValue != None):
            self._strength = newValue
        else:
            return self._strength
    def innitiative(self):
        return self._innitiative
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

    @abc.abstractmethod
    def action(self):
        ...
    @abc.abstractmethod
    def collision(self):
        ...
    @abc.abstractmethod
    def displayChar(self):
        ...

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
        self._world.add_organism(newOrganism)

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
                
                # Message message1 = new Message(), message2 = new Message();
                # message1.addToList( thisOrganism.getClass().getSimpleName());
                # message2.addToList( otherOrganism.getClass().getSimpleName());

            
                # message1.addToList( thisOrganism.getKillMessage());
                # message2.addToList( otherOrganism.getKillMessage());

                # message1.addToList( otherOrganism.getClass().getSimpleName());
                # message2.addToList( thisOrganism.getClass().getSimpleName());
                #TODO

                # world.manager().pushMessage(message1);
                # world.manager().pushMessage(message2);
                

                thisOrganism.die()
                otherOrganism.die()
                return

            # Message message = new Message();
            # message.addToList(thisOrganism.getClass().getSimpleName()); 
            # message.addToList(thisOrganism.getKillMessage());
            # message.addToList(otherOrganism.getClass().getSimpleName());

            # world.manager().pushMessage(message);
            #TODO
            
            newPosX = otherOrganism.positionX()
            newPosY = otherOrganism.positionY()
            otherOrganism.die()

            self.moveOrganism(newPosX, newPosY)

        if(thisCollision.escapeAfterFailedAttack and action.thisAttackerStrength < action.otherDefenderStrength):

            positionX = self.positionX()
            positionY = self.positionY()
            
            # ArrayList <Vector> directions = world.aiDirections();
            # ArrayList <Vector> emptyCells = new ArrayList<Vector>();
        
            # Organism targetOrganism;
            # Vector coordinate = new Vector(0, 0);
            # //Find empty cell to escape to
            # for(int i=0; i < directions.size(); ++i)
            # {
            #     coordinate.x = positionX + directions.get(i).x;
            #     coordinate.y = positionY + directions.get(i).y;
            #     if(!world.isInBounds(coordinate))
            #         continue;
            #     targetOrganism = world.boardCells().get(coordinate.x).get(coordinate.y);
            #     if(targetOrganism == null)
            #     {
            #         Vector newVector = new Vector(coordinate.x, coordinate.y);
            #         emptyCells.add(newVector);
            #     } 
            # }
            
            # if(emptyCells.size() == 0)
            #     return;
            # Random rand = new Random();
            # Vector direction = emptyCells.get(rand.nextInt(emptyCells.size()));
            #TODO
            
            #moveOrganism(direction.x, direction.y);
            
            return
            
        if(action.otherAttackerStrength > action.thisDefenderStrength):

            if(thisCollision.givesStrength):
                otherOrganism.strength(otherOrganism.strength() + thisCollision.givenStrength)
            
            # Message message = new Message();
            # message.addToList(otherOrganism.getClass().getSimpleName()); 
            # message.addToList(otherOrganism.getKillMessage());
            # message.addToList(thisOrganism.getClass().getSimpleName());

            #world.manager().pushMessage(message);
            # TODO
            thisOrganism.die()
        
    
