from .. import animal 

class CyberSheep(animal.Animal):
    def __init__(self, positionX, positionY):
        super(CyberSheep, self).__init__(positionX, positionY, 11, 4)
    def displayChar(self):
        return "C"