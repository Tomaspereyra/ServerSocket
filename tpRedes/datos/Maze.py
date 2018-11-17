# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

PISO = 0
PARED = 1
GUARDIA = 2
HERO = 3
SALIDA = 4
ORO = 5
LLAVE = 6

FOG_DISTANCE = 2

from datos.Hero import Hero



class Maze :

    WIDTH = 16
    HEIGHT = 16



    def __init__(self):
        self.tiles = [[0 for x in range(self.WIDTH)] for x in range(self.HEIGHT)]
        self.hero = None

    def getTile(self, x, y):
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
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
            #print("Read row : " + rows[row])
            for col in range(self.HEIGHT):
                self.tiles[col][row] = int(rows[row][col])
                if self.tiles[col][row] == HERO:
                    self.hero = Hero(col, row, self)

    def tileToString(self, tile):
        result = "X"

        if tile == PISO:
            result = "C"
        elif tile == PARED:
            result = "P"
        elif tile == HERO:
            result = "@"
        elif tile == LLAVE:
            result = "K"
        elif tile == SALIDA:
            result = "S"
        elif tile == GUARDIA:
            result = "G"
        elif tile == ORO:
            result = "O"
        return result

    def squareDistance(self, x1, y1, x2, y2):
        xDist = abs(x2 - x1)
        yDist = abs(y2 - y1)
        return max(xDist, yDist)

    def toString(self):
        result = ""
        for row in range(self.WIDTH):
            for col in range(self.HEIGHT):

                if self.squareDistance(col, row, self.hero.x, self.hero.y) <= FOG_DISTANCE:
                    result += self.tileToString(self.tiles[col][row])
                else:
                    result += " "
            result += "\n"
        return result

