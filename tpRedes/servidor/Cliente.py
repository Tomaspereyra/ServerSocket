import SimpleHTTPServer
import socket
import os
from msvcrt import getch

CONTINUE = 0
LOST = 1
WON = 2

class Cliente:

    def __init__(self, host, port):
        self.socketCliente = socket.socket()
        self.socketCliente.connect((host, port))

    def enviarDatos(self):
        login = raw_input("Ingrese usuario y contrasena:")
        self.socketCliente.send(login)
        respuesta = self.socketCliente.recv(1024)
        print respuesta
        print self.socketCliente.recv(1024)
        entrada = ''
        while entrada !='e':

            entrada = getch()
            if entrada != 'e':
                os.system('cls')
                self.socketCliente.send(str(entrada))
                respuesta = self.socketCliente.recv(1024)
                respuestas = respuesta.split("/")

                mapa = respuestas[0]
                status = int(respuestas[2])
                msg = respuestas[3]

                print mapa
                print msg

                if status != CONTINUE:
                    entrada = 'e'
                    if status ==  WON:
                        print "Ganaste el juego!"
                    elif status == LOST:
                        print "Perdiste el juego!"

        print "Juego Terminado! Juegue otra vez!"

        self.socketCliente.close()


cliente = Cliente("localhost",8000)
cliente.enviarDatos()