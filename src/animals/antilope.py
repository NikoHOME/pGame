from .. import animal 

class Antilope(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Antilope, self).__init__(positionX, positionY, 4, 4)
    def displayChar(self):
        return "A"
    def name(self):
        return "Antilope"
    def action(self):
        self.basicMovementHandle()
        self.basicCollisionHandle()
        #TODO

    