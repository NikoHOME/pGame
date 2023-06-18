#from . import organism
from .functions import SpawnInfo
from .functions import Vector2
from .functions import str_to_class

from .animals.sheep import Sheep
from .animals.wolf import Wolf
from .animals.antilope import Antilope
from .animals.player import Player
from .animals.fox import Fox
from .animals.cyberSheep import CyberSheep
from .animals.turtle import Turtle

from .plants.grass import Grass
from .plants.belladona import Belladona
from .plants.dandelion import Dandelion
from .plants.hogweed import Hogweed
from .plants.guarana import Guarana

import random

import abc
class World(abc.ABC):
    index = 0
    def __init__(self, width, height, manager, populateFlag = True):
        self._height = height
        self._width = width
        self._manager = manager
        self._board = [[ None for y in range(height)] for x in range(width)]


        self._player = None
        self._playerAlive = True
        self._playerAbilityOn = False
        self._playerAbilityAvaible = True
        self._playerAbilityDuration = 5
        self._playerAbilityDelay = 10
        self._playerAbilityTimeUsed = -10
        self._turn = 0
        if(populateFlag):
            self.populate_world()

    def copyWorldData(self):
        from .functions import WorldData
        
        data = WorldData()

        data.playerAlive = self._playerAlive
        data.playerAbilityOn = self._playerAbilityOn
        data.playerAbilityAvaible = self._playerAbilityAvaible

        data.playerAbilityTimeUsed = self._playerAbilityTimeUsed
        data.turn = self._turn

        data.width = self._width
        data.height = self._height
        data.isHex = self.isHex

        data.board = [[ None for y in range(data.height)] for x in range(data.width)]

        organisms = 0
        for x in range(data.width):
            for y in range(data.height):
                if(self._board[x][y] != None):
                    data.board[x][y] = self._board[x][y]
                    organisms += 1
        data.organisms = organisms        
        return data


    def playerAbilityTimeLeft(self):
        if(self._playerAbilityTimeUsed + self._playerAbilityDuration < self._turn):
            return 1
        else:
            return self._playerAbilityTimeUsed + self._playerAbilityDuration - self._turn

    def playerAbilityAvaible(self, newValue = None):
        if(newValue == None):
            return self._playerAbilityAvaible
        else:
            self._playerAbilityAvaible = newValue
    def playerAbilityOn(self, newValue = None):
        if(newValue == None):
            return self._playerAbilityOn
        else:
            self._playerAbilityOn = newValue
    def playerAlive(self):
        return self._playerAlive
    def turn(self, newValue = None):
        if(newValue == None):
            return self._turn
        else:
            self._turn = newValue
    def height(self):
        return self._height
    def width(self):
        return self._width
    def manager(self):
        return self._manager
    def board(self):
        return self._board
    def directions(self):
        return self._directions
    def directionsDiagonal(self):
        return self._directionsDiagonal
    def player(self, newValue = None):
        if(newValue == None):
            return self._player
        else:
            self._player = newValue

    def isInBounds(self, coordinate):
        if(coordinate.x >= 0 and coordinate.x < self._width):
            if(coordinate.y >= 0 and coordinate.y < self._height):
                return True
        return False

    def print(self):
        for x in range(0, self.width()):
            for y in range(0, self.height()):
                if(self.board()[x][y] != None):
                    print(f'({self.board()[x][y].strength()}, {self.board()[x][y].innitiative()})', end="")
                else:
                    print(f'(X, X)', end="")
            print("")

    def add_organism(self, organism):
        organism.isDead(False)
        organism.index(self.index)
        organism.world(self)
        self.index += 1
        self.board()[organism.positionX()][organism.positionY()] = organism
        self.update()

    def playerUseAbility(self):
        self._playerAbilityOn = True
        self._playerAbilityTimeUsed = self._turn
        self._playerAbilityAvaible = False

    def nextTurn(self):
        self._turn +=1

    def update(self):
        if(self._player != None):
            if(self._board[self._player.positionX()][self._player.positionY()] != self._player):
                self._player = None
                self._playerAlive = False
                self._playerAbilityTimeUsed = -10
            else:
                self._playerAlive = True
        else:
            self._playerAlive = False

        if(self._playerAbilityTimeUsed + self._playerAbilityDelay <= self._turn):
            self._playerAbilityAvaible = True
        else:
            self._playerAbilityAvaible = False
        
        if(self._playerAbilityTimeUsed + self._playerAbilityDuration < self._turn):
            self._playerAbilityOn = False

    def populate_world(self):
        emptyList = []

        for x in range(0, self.width()):
            for y in range(0, self.height()):
                emptyList.append(Vector2(x, y))

        organismList = [
            SpawnInfo("Fox", 3),
            SpawnInfo("Wolf", 1),
            SpawnInfo("Sheep", 2),
            SpawnInfo("Turtle", 2),
            SpawnInfo("CyberSheep", 1),
            SpawnInfo("Antilope", 1),

            SpawnInfo("Grass", 3),
            SpawnInfo("Guarana", 2),
            SpawnInfo("Hogweed", 1),
            SpawnInfo("Belladona", 1),
            SpawnInfo("Dandelion", 1),
        ]

        randomInt = random.randint(0, len(emptyList)-1)
        organism = Player(emptyList[randomInt].x, emptyList[randomInt].y)
        self.add_organism(organism)
        self._player = organism
        emptyList.pop(randomInt)
        
        average = round(self.width() * self.height() / 24) 

        for organismInfo in organismList:
            ammount = random.randint(1, average * organismInfo.multiplier)
            for i in range(0, ammount):
                randomInt = random.randint(0, len(emptyList)-1)
                organism = str_to_class(organismInfo.name)(emptyList[randomInt].x, emptyList[randomInt].y)
                self.add_organism(organism)
                emptyList.pop(randomInt)
                if(len(emptyList) == 0):
                    break
            if(len(emptyList) == 0):
                    break
    