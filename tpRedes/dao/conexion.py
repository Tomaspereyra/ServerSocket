import MySQLdb


class Sesion:
     def __init__(self):
         self.estado = MySQLdb.connect(host="localhost", user="root", passwd="root", db="bdredes")


     def getEstado(self):
        return self.estado

     def obtenerCursor(self):

        return self.getEstado().cursor()

     def commit(self):
        self.getEstado().commit()

     def cerrarConexion(self):

        return self.getEstado().close()