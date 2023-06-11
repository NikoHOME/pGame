from .. import animal 

class Sheep(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Sheep, self).__init__(positionX, positionY, 4, 4)
    def displayChar(self):
        return "S"