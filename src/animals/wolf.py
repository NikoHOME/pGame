from .. import animal 

class Wolf(animal.Animal):
    def __init__(self, positionX, positionY):
        super(Wolf, self).__init__(positionX, positionY, 9, 5)
    def displayChar(self):
        return "W"
    def name(self):
        return "Wolf"
    def displayColour(self):
        return (190, 190, 180, 170)