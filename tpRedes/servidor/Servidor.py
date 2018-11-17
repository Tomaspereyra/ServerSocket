
import SocketServer,socket
import threading
from datos.Maze import *
from datos.Hero import MoveResult
from dao.UsuarioDao import UsuarioDao

TIMEOUT = 10

testMap = "2005551111111111\n0111111115000005\n0111111111110111\n0142000111110111\n0111110111110115\n0111110111110110\n0130000111110000\n0111110111110111\n0000000111110111\n0111110111110111\n0100000000025555\n0111111111112111\n0000000111112111\n1111000111112111\n1111005111112111\n1111111111112226"

class server:

      def __init__(self):

          server = ThreadedTCPServer(("localhost", 8000), Handler)

          print "Server en el puerto", 8000
          server.serve_forever()

NORMAL = 0
CONSOLA = 1
class Handler(SocketServer.BaseRequestHandler):

    def parsearMensajeLog(self, data):
        splitData = data.split("|")
        return splitData[0], splitData[1], splitData[2], splitData[3]

    def handle(self):

        threadName = threading.currentThread().getName()
        activeThreads = threading.activeCount() - 1
        clientIP = self.client_address[0]
        print '[%s] -- New connection from %s -- Active threads: %d' % (threadName, clientIP, activeThreads)
        data = self.request.recv(1024)
        print '[%s] -- %s -- Received: %s' % (threadName, clientIP, data)

        #Armar While hasta que loguee con exito. Una vez hecho
        #yo obtengo el Tipo y decido a que juego va
        log = False
        tipo = 0
        while log == False:
            comando, cuenta, password, tipo = self.parsearMensajeLog(data)
            if comando == "LOG":
                log = self.login(cuenta, password)
            if (tipo < 0) or (tipo > 1):      #este if me volvio loco
                print "tipo incorrecto: ", tipo
               # log = False           #si sacas este comentario en log, no pasa nunca, aunque tipo este bien
            if log == False:
                self.request.send("LOG|ERROR")
                data = self.request.recv(1024)
        self.request.send("LOG|OK")
            #Volver al loop, tipo incorrecto. Evalua esto junto a la pw y eso como
            #otra condicion de que este todo mal.

        map = testMap


        maze = Maze()
        maze.fromString(map)
        self.request.send(maze.toString())
        hero = maze.hero

        if tipo == NORMAL:
            self.enterNormalGameMode(maze, hero)
        elif tipo == CONSOLA:
            self.enterConsoleGameMode(maze, hero)

    def login(self, cuenta, password):

        usuario = UsuarioDao()
        u = usuario.traerUsuario(cuenta)

        if u is not None and u.getContrasena() == password:
            return True
        else:
            return False

    def enterConsoleGameMode(self, maze, hero):
        mov = ''
        terminado = False
        while not terminado:
            try:
                mov = self.request.recv(1024).strip()
                if not terminado:
                    result = self.procesarMovimientoConsola(mov, hero)
                    if result:
                        terminado = result.status != 0
                        self.enviarMensajeJuegoConsola(maze.toString() + "/" + result.serialize())
                    else:
                        self.enviarMensajeErrorConsola(mov, hero, maze)
            except:
                print ("Error : " + mov)
                self.enviarMensajeErrorConsola(mov, hero, maze)

    def enterNormalGameMode(self, maze, hero):
        mov = ''
        while mov != 'e':
            try:
                mov = self.request.recv(1024).strip()
                if mov != 'e':
                    result = self.procesarMovimientoTecla(mov, hero)
                    if result:
                        self.request.send(maze.toString() + "/" + result.serialize())
                    else:
                        self.enviarMensajeErrorNormal(mov, hero, maze)
            except:
                print ("Error : " + mov)
                self.enviarMensajeErrorNormal(mov, hero, maze)

    def enviarMensajeErrorNormal (self, mov, hero, maze):
        self.request.send(maze.toString() + "/" + self.makeErrorResult(mov, hero).serialize())

    def enviarMensajeErrorConsola (self, mov, hero, maze):
        self.enviarMensajeJuegoConsola(maze.toString() + "/" + self.makeErrorResult(mov, hero).serialize())

    def enviarMensajeJuegoConsola (self, msg):
        self.request.send("RESULT|" + msg)

    def makeErrorResult(self, msg, hero):
        return MoveResult(False, "ERROR en la solicitud de mensaje : '" + msg.replace("|", "I") + "'", hero)



    def esMensajeConsola(self, movimiento):
        return movimiento.find("|") != -1

    def parsearMensajeConsola(self, mensaje):
        if (len(mensaje) > 1):
            msgSplit = mensaje.split("|")
            comando = msgSplit[0]
            datos = msgSplit[1]
        else:
            comando = ""
            datos = ""
        return comando, datos

    def juego(self, movimiento, hero):

        if self.esMensajeConsola(movimiento):
            return self.procesarMovimientoConsola(movimiento, hero)
        else:
            return self.procesarMovimientoTecla(movimiento, hero)


    def procesarMovimientoTecla(self, movimiento, hero):
        if movimiento == 'd':
            return hero.moveRight()
        if movimiento == 'a':
            return hero.moveLeft()
        if movimiento == 's':
            return hero.moveDown()
        if movimiento == 'w':
            return hero.moveUp()
        else:
            return None

    def procesarMovimientoConsola(self, movimiento, hero):

        comando, datos = self.parsearMensajeConsola(movimiento)
        print ("Comando : " + comando)
        print ("Datos : " + datos)
        if comando == "MOVE":
            if datos == 'RIGHT':
                return hero.moveRight()
            if datos == 'LEFT':
                return hero.moveLeft()
            if datos == 'DOWN':
                return hero.moveDown()
            if datos == 'UP':
                return hero.moveUp()
        else:
            #Comando invalido
            return None



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


serv = server()


