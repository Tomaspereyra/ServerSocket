# coding=utf-8
import MySQLdb
from dao.conexion import Sesion
from datos.Usuario import Usuario


class UsuarioDao:

    def iniciaOperacion(self):
        try:
             sesion = Sesion()

        except MySQLdb.OperationalError:
            print "Error al iniciar la sesion con la base de datos"
            sesion =None

        return sesion

    def agregarUsuario(self, nombre, contrasena):
        sesion = self.iniciaOperacion()

        cursor = sesion.obtenerCursor()

        try:

            cursor.execute("""insert into Usuario (nombre, contraseña) values ('%s','%s')""" % (nombre , contrasena))
            sesion.commit()
        except:
            print "Error registrando usuario"
            sesion.getEstado().rollback()
        finally:
            cursor.close()
            sesion.cerrarConexion()

    def traerUsuarios(self):
        sesion = self.iniciaOperacion()
        cursor = sesion.obtenerCursor()
        resultado = []
        usuario = Usuario()
        lstUsuarios = []

        try:
            cursor.execute("""select * from Usuario order by idUsuario asc""")
            resultado = cursor.fetchall()
            for fila in range(len(resultado)):
                for columna in range(len(resultado[fila])):
                    if columna == 0:
                        usuario.setIdUsuario(resultado[fila][columna])
                    if columna == 1:
                        usuario.setNombre(resultado[fila][columna])
                    if columna == 2:
                        usuario.setContrasena(resultado[fila][columna])
                        lstUsuarios.append(usuario)
                        usuario = Usuario()

        finally:
            cursor.close()
            sesion.cerrarConexion()

        return lstUsuarios

    def traerUsuario(self, username):
        sesion = self.iniciaOperacion()
        cursor = sesion.obtenerCursor()
        usuario = None
        try:
            cursor.execute("""select * from Usuario where Usuario.nombre='%s'""" % username)
            resultado = cursor.fetchone()
            if resultado is not None:
                usuario = Usuario(resultado[1], resultado[2])
                usuario.setIdUsuario(resultado[0])
        except:
            print "Error, no se pudo traer el usuario"
        finally:
            cursor.close()
            sesion.cerrarConexion()

        return usuario



