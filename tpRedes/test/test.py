from datos.Maze import *

map = "3114\n0110\n0110\n0000"


def main():
    print("main()...")
    maze = Maze()
    maze.fromString(map)
    hero = maze.hero
    print(maze.toString())


    print (str(hero.moveDown()))

    print(maze.toString())

    print(str(hero.moveDown()))

    print(maze.toString())
    print(str(hero.moveRight()))

    print(maze.toString())
    print(str(hero.moveDown()))

    print(maze.toString())
    print(str(hero.moveRight()))

    print(maze.toString())


if __name__ == "__main__":
    main()
