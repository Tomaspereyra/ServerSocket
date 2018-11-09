# coding=utf-8
__author__ = "Martin Rios"
__copyright__ = "None"
__credits__ = ["Martin Rios", "Gonzalo Montaña", "Ignacio Oliveto"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Martin Rios"
__email__ = "riosmartin93@gmail.com"
__status__ = "Prototype"

from datos.Maze import *

CONTINUE = 0
LOST = 1
WON = 2

class MoveResult:
    def __init__(self, success, msg, hero):
        self.success = success
        self.msg = msg
        self.hero = hero

    def getStatus(self):
        if not self.hero.alive:
            return LOST
        elif self.hero.won:
            return WON
        else:
            return CONTINUE

    def serialize(self):
        return str(self.success) + "/" + \
               str(self.getStatus()) + "/" + \
               str(self.msg) + "/" + \
               str(self.hero.gold) + "/" + \
               str(self.hero.llave)

class Hero:

    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.gold = 0
        self.alive = True
        self.won = False
        self.llave = False

    def moveRight(self):
        return self.move(1, 0)

    def moveLeft(self):
        return self.move(-1, 0)

    def moveUp(self):
        return self.move(0, -1)

    def moveDown(self):
        return self.move(0, 1)



    def move(self, x, y):
        tile = self.maze.getTile(self.x     + x, self.y + y)
        print ("Current pos : " + str(self.x) + "," + str(self.y) + " - Moving to : " + str(self.x + x) + "," + str(self.y + y) + " - Destination Tile : " + str(tile))
        if tile is None or tile == PARED:
            return MoveResult(False, "¡Te chocaste contra la pared!", self)
        elif tile == GUARDIA:
            if self.gold == 0:
                self.kill()
                return MoveResult(False, "Fuiste asesinado por un guardia!", self)
            else:
                self.gold -= 1
                self.place(self.x + x, self.y + y)
                return MoveResult(True, "El guardia te deja pasar por una moneda de oro!", self)
        elif tile == LLAVE:
            self.llave = True
            self.place(self.x + x, self.y + y)
            return MoveResult(True,"Conseguiste la Llave! ¡Ahora encuentra la salida!", self)
        elif tile == ORO:
            self.gold += 1
            self.place(self.x + x, self.y + y)
            return MoveResult(True, "Conseguiste una moneda de oro! Ahora tienes " + str(self.gold) + " Monedas de oro!", self)
        elif tile == SALIDA:
            self.place(self.x + x, self.y + y)
            if self.llave:
                self.won = True
                return MoveResult(True, "Llegaste a la salida!", self)
            else:
                return MoveResult(True, "Necesitas una llave para salir!", self)

        elif tile == PISO:
            self.place(self.x + x, self.y + y)
            return MoveResult(True, "Te desplazaste con exito!", self)
        else:
            return MoveResult(True, "Error en la matrix!", self)

    def kill(self):
        self.alive = False

    def place(self, x, y):
        self.maze.setTile(self.x, self.y, PISO)
        self.maze.setTile(x, y, HERO)
        self.x = x
        self.y = y