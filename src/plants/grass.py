from .. import plant 

class Grass(plant.Plant):
    def __init__(self, positionX, positionY):
            super(Grass, self).__init__(positionX, positionY, 0)
    def displayChar(self):
        return "^"
    def name(self):
        return "Grass"