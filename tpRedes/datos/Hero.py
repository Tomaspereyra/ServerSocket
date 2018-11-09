from datos.Maze import *
class Hero:

    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.gold = 0
        self.alive = True
        self.won = False

    def moveRight(self):
        return self.move(1, 0)

    def moveLeft(self):
        return self.move(-1, 0)

    def moveUp(self):
        return self.move(0, -1)

    def moveDown(self):
        return self.move(0, 1)

    def move(self, x, y):
        tile = self.maze.getTile(self.x + x, self.y + y)
        print ("Current pos : " + str(self.x) + "," + str(self.y) + " - Moving to : " + str(self.x + x )+ "," + str(self.y + y) + " - Destination Tile : " + str(tile))
        if tile is None or tile == PARED:
            return False
        elif tile == GUARDIA:
            if self.gold == 0:
                self.kill()
                return False
            else:
                self.gold -= 1
        elif tile == ORO:
            self.gold += 1
        elif tile == SALIDA:
            self.won = True

        self.place(self.x + x, self.y + y)
        return True

    def kill(self):
        self.alive = False

    def place(self, x, y):
        self.maze.setTile(self.x, self.y, PISO)
        self.maze.setTile(x, y, HERO)
        self.x = x
        self.y = y