import organism as org

class World:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.board = [[ org.Organism(x, y, -1, -1) for y in range(height)] for x in range(width)]
    def print(self):
        for row in self.board:
            for cell in row:
                print(f'({cell.strength}, {cell.innitiative})', end="")
            print("")