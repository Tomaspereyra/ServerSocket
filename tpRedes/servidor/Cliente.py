import SimpleHTTPServer
import socket
import os
from msvcrt import getch

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
       exit = ''
       while exit !='e':

           exit = getch()
           os.system('cls')
           self.socketCliente.send(str(exit))
           respuesta = self.socketCliente.recv(1024)
           print respuesta

       self.socketCliente.close()


cliente = Cliente("localhost",8000)
cliente.enviarDatos()