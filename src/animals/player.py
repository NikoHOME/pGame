from .. import animal 

class Player(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Player, self).__init__(positionX, positionY, 5, 4)
    def displayChar(self):
        return "P"