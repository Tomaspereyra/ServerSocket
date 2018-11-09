
import SocketServer,socket
import threading
from datos.Maze import *

TIMEOUT = 10

testMap = "2005551111111111\n0111111115000005\n0111111111110111\n0142000111110111\n0111110111110115\n0111110111110110\n0130000111110000\n0111110111110111\n0000000111110111\n0111110111110111\n0100000000025555\n0111111111112111\n0000000111112111\n1111000111112111\n1111005111112111\n1111111111112226"

class server:

      def __init__(self):

          server = ThreadedTCPServer(("localhost", 8000), Handler)

          print "Server en el puerto", 8000
          server.serve_forever()


class Handler(SocketServer.BaseRequestHandler):

    def handle(self):

        threadName = threading.currentThread().getName()
        activeThreads = threading.activeCount() - 1
        clientIP = self.client_address[0]
        print '[%s] -- New connection from %s -- Active threads: %d' % (threadName, clientIP, activeThreads)
        data = self.request.recv(1024)
        print '[%s] -- %s -- Received: %s' % (threadName, clientIP, data)

        #map = "3114\n0110\n0110\n0060"
        map = testMap
        self.request.send(self.login(data)) #implementar login aca

        maze = Maze()
        maze.fromString(map)
        self.request.send(maze.toString())
        hero = maze.hero
        mov = ''
        while mov != 'e':
            mov = self.request.recv(1024).strip()
            if (mov != 'e'):
                result = self.juego(mov, hero)
                self.request.send(maze.toString() + "/" + result.serialize())

    def login(self, msj):

        inicioDePalabra = 0
        for i in range(len(msj)):

            if msj[i] == ' ' or i == len(msj)-1:

                usuario = msj[inicioDePalabra:i+1]
                inicioDePalabra = i+1

        return "Bienvenido"



    def juego(self, movimiento, hero):


        if movimiento == 'd':
            return hero.moveRight()
        if movimiento == 'a':
            return hero.moveLeft()
        if movimiento == 's':
            return hero.moveDown()
        if movimiento == 'w':
            return hero.moveUp()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)




serv = server()


