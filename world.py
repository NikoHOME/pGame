import organism as org

class World:
    index = 0
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.board = [[ None for y in range(height)] for x in range(width)]

    def print(self):
        for row in self.board:
            for cell in row:
                if(cell != None):
                    print(f'({cell.strength}, {cell.innitiative})', end="")
                else:
                    print(f'(X, X)', end="")
            print("")

    def add_organismn(self, organism):
        organism.isDead = False
        organism.index = self.index
        self.index += 1
        self.board[organism.positionX][organism.positionY] = organism

    