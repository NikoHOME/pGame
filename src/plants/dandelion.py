from .. import plant 

class Dandelion(plant.Plant):
    def __init__(self, positionX, positionY):
            super(Dandelion, self).__init__(positionX, positionY, 0)
    def displayChar(self):
        return "D"
    def action(self):
        for i in range(0, 3): # 3 Tries to grow
            if(self.basicGrowHandle() == True):
                return