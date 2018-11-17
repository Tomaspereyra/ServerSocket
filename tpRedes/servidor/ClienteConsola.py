import SimpleHTTPServer
import socket
import os
import sys
from msvcrt import getch
import sys
try:
   import colorama
   colorama.init()
except:
   try:
       import tendo.ansiterm
   except:
       pass

CONTINUE = 0
LOST = 1
WON = 2


class bcolors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[34m"
    CYAN = "\033[96m"
    WHITE = "\033[37m"
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Cliente:



    def __init__(self, host, port):
        self.socketCliente = socket.socket()
        self.socketCliente.connect((host, port))

    def enviarDatos(self):
        log = False
        while log == False:
            login = raw_input("Ingrese usuario y contrasena:")
            self.socketCliente.send(login)
            respuesta = self.socketCliente.recv(1024)
            print respuesta
            if respuesta == "LOG|OK":
                log = True

        #self.imprimirMapa(respuesta)
        os.system('cls')
        self.imprimirMapa(self.socketCliente.recv(1024))
        entrada = ''
        terminado = False
        while not terminado:
            print ("Ingrese el mensaje : ")
            entrada = raw_input()
            if not terminado:
                os.system('cls')
                self.socketCliente.send(str(entrada))
                respuesta = self.socketCliente.recv(1024)
                #print "Respuesta : " + respuesta
                try:
                    comando, msg = self.parsearMensajeConsola(respuesta)
                    respuestas = msg.split("/")

                    mapa = respuestas[0]
                    status = int(respuestas[2])
                    msg = respuestas[3]
                    oro = respuestas[4]
                    if respuestas[5] == "True":
                        tieneLlave = "SI"
                    else:
                        tieneLlave = "NO"

                    self.imprimirMapa (mapa)
                    print "ORO : " + oro + " - Llave : " + tieneLlave
                    print msg
                except:
                    print("Ocurrio un error")
                    status = CONTINUE
                if status != CONTINUE:
                    terminado = True
                    if status ==  WON:
                        print "Ganaste el juego!"
                    elif status == LOST:
                        print "Perdiste el juego!"

        print "Juego Terminado! Juegue otra vez!"

        self.socketCliente.close()

    def parsearMensajeConsola(self, mensaje):
        #print("mensaje recibido : " + mensaje)
        try:
            if len(mensaje) > 1:
                msgSplit = mensaje.split("|")
                comando = msgSplit[0]
                datos = msgSplit[1]
            else:
                comando = ""
                datos = ""
        except:
            comando = ""
            datos = ""
        return comando, datos

    def imprimirMapa(self, mapa):
        sys.stdout.flush()
        for ch in mapa:
            if ch != "\n":
                sys.stdout.write(self.imprimirColor(ch) + ch + self.imprimirFinColor())
            else:
                sys.stdout.write(ch)

    def imprimirColor(self, ch):
        if ch == "@":
            return bcolors.GREEN
        elif ch == "G":
            return bcolors.RED
        elif ch == "E" or ch == "S" or ch=="K":
            return bcolors.CYAN
        elif ch == "O":
            return bcolors.YELLOW
        elif ch == "C":
            return bcolors.WHITE
        else:
            return bcolors.BOLD

    def imprimirFinColor(self):
        return bcolors.ENDC

cliente = Cliente("localhost",8000)
cliente.enviarDatos()