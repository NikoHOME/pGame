import sys

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

def str_to_class(str):
    return getattr(sys.modules[__name__], str)

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if(other == None):
            return False
        return self.x == other.x and self.y == other.y

class SpawnInfo:
    def __init__(self, name, multiplier):
        self.name = name
        self.multiplier = multiplier

class QueueInfo:
    def __init__(self, innitiative, age, organism):
        self.innitiative = innitiative
        self.age = age
        self.organism = organism
    def __lt__(self, other):
        if(self.innitiative < other.innitiative):
            return False
        elif(self.age > other.age and self.innitiative == other.innitiative):
            return False
        return True


class CollisionAction:
    def __init__(self):
        self.realStrength = 0
        self.tempAttackStrength = -1
        self.tempDefenceStrength = -1
        self.hasTempAttackStrength = False
        self.hasTempDefenceStrength = False
        self.givenStrength = -1
        self.givesStrength = False
        self.escaped = False
        self.killAfterDefeat = False
        self.escapeAfterFailedAttack = False
        self.isImmortal = False
        self.isImmuneToHogweed = False
        self.isHogweed = False

class AttackAction: 
    def __init__(self):
        self.thisAttackerStrength = -1
        self.thisDefenderStrength = -1
        self.otherAttackerStrength = -1
        self.otherDefenderStrength = -1


class WorldData:
    def __init__(self):

        self.playerAlive = False
        self.playerAbilityOn = False
        self.playerAbilityAvaible = False
        self.playerAbilityTimeUsed = 0

        self.turn = 0

        self.height = 0
        self.width = 0
        self.isHex = False

        self.board = None
        self.organisms = 0


