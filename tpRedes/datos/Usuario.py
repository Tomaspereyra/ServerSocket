class Usuario:

    def __init__(self, nombre="", contrasena=""):
        self.nombre = nombre
        self.contrasena = contrasena

    def getNombre(self):
        return self.nombre

    def setNombre(self, nombre):
        self.nombre = nombre

    def setContrasena(self,contrasena):
        self.contrasena = contrasena

    def getContrasena(self):
        return self.contrasena

    def setIdUsuario(self, idusuario):
        self.idUsuario =idusuario

    def getIdUsuario(self):
        return self.idUsuario

    def __str__(self):
        return str(self.nombre)