
import SocketServer

from datos.Maze import *


class server:

      def __init__(self):

          httpd = SocketServer.TCPServer(("localhost", 8000), Handler)

          print "Server en el puerto", 8000
          httpd.serve_forever()


class Handler(SocketServer.BaseRequestHandler):

    def handle(self):
        map = "3114\n0110\n0110\n0000"
        self.datos = self.request.recv(1024).strip()
        self.login(self.datos)
        self.request.send(self.login(self.datos))

        exit = ""
        maze = Maze()
        maze.fromString(map)
        self.request.send(maze.toString())
        hero = maze.hero

        while exit != 'e':
            mov = self.request.recv(1024).strip()
            self.juego(mov, hero)
            self.request.send(maze.toString())

    def login(self, msj):

        inicioDePalabra = 0
        for i in range(len(msj)):

            if msj[i] == ' ' or i == len(msj)-1:

                usuario = msj[inicioDePalabra:i+1]
                inicioDePalabra = i+1
                print usuario
        return "Bienvenido"



    def juego(self, movimiento, hero):


        if movimiento == 'd':
            hero.moveRight()
        if movimiento == 'a':
            hero.moveLeft()
        if movimiento == 's':
            hero.moveDown()
        if movimiento == 'w':
            hero.moveUp()

    def test(self):
        map = "3114\n0110\n0110\n0000"
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



serv = server()


