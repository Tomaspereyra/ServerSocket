PISO = 0
PARED = 1
GUARDIA = 2
HERO = 3
SALIDA = 4
ORO = 5

from datos.Hero import Hero



class Maze :

    WIDTH = 4
    HEIGHT = 4

    def __init__(self):
        self.tiles = [[0 for x in range(self.WIDTH)] for x in range(self.HEIGHT)]
        self.hero = None

    def getTile(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y > self.HEIGHT:
            return None
        else:
            return self.tiles[x][y]

    def setTile(self, x, y, val):
        if x < 0 or x >= self.WIDTH or y < 0 or y > self.HEIGHT:
            raise ValueError('Position input is out of bounds.')
        else:
            self.tiles[x][y] = val

    def fromString(self, mapString):
        rows = mapString.splitlines()

        for row in range(self.WIDTH):
            print("Read row : " + rows[row])
            for col in range(self.HEIGHT):
                self.tiles[col][row] = int(rows[row][col])
                if self.tiles[col][row] == HERO:
                    self.hero = Hero(col, row, self)

    def tileToString(self, tile):
        result = "X"

        if tile == PISO:
            result = "'"
        elif tile == PARED:
            result = "#"
        elif tile == HERO:
            result = "@"
        elif tile == SALIDA:
            result = "<"
        elif tile == GUARDIA:
            result = "G"
        elif tile == ORO:
            result = "O"
        return result

    def toString(self):
        result = ""
        for row in range(self.WIDTH):
            for col in range(self.HEIGHT):
                result += self.tileToString(self.tiles[col][row])
            result += "\n"
        return result

