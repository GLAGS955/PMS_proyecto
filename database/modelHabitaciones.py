
class ModelHabitaciones:

    @classmethod
    #funcion Principal
    def Obtener_habitaciones(cls, db) -> list:
        cursor = None

        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_habitacion, codigo, tipo, descripcion, estado, capacidad, precio, grado, url_foto
                    FROM habitaciones"""
            cursor.execute(sql)
            filas = cursor.fetchall()

            habitaciones = []

            for fila in filas:
                habitaciones.append({
                    "id_habitacion": fila[0],
                    "codigo": fila[1],
                    "tipo": fila[2],
                    "descripcion": fila[3],
                    "estado": fila[4],
                    "capacidad": fila[5],
                    "precio": fila[6],
                    "grado": fila[7],
                    "foto": fila[8]
                    })
            return habitaciones
                
        except Exception as ex:
            raise ValueError(f"Error de obtener habitaciones {ex}")
        finally:
            if cursor:
                cursor.close()

    #funcion para la logica de reservaciones, modidifica estado de la tabla de habitaciones
    @classmethod
    def Modificar_estado(cls, db, estado, id_habitacion):
        cursor = None

        try:
            cursor = db.connection.cursor()
            sql = "UPDATE habitaciones SET estado = %s WHERE id_habitacion = %s"
            cursor.execute(sql,(estado,id_habitacion))
            db.connection.commit()

            return cursor.rowcount > 0

        except Exception as ex:
            raise ValueError(f"Error de actualizacion de estados de habitaciones {ex}")
            
        finally:
            if cursor:
                cursor.close()

    #funcion de control para evitar duplicados de codigos de las habitaciones
    @classmethod
    def verificar_codigo(cls, db,codigo):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_habitacion FROM habitaciones WHERE codigo = %s"

            cursor.execute(sql, (codigo,))
            row = cursor.fetchone()

            if row is not None:
                return True
            return False

        except Exception as ex:
            print(f"Error al verificar el código de la habitación: {ex}")
            raise ValueError("Error al verificar disponibilidad del código") from ex

        finally:
            if cursor:
                cursor.close()

#Funcion principal
    @classmethod
    def agregar_habitacion(cls, db, nueva_habitacion):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO habitaciones (codigo, tipo, descripcion, estado, capacidad, precio, grado, url_foto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, nueva_habitacion)
            db.connection.commit()
            return True

        except Exception as ex:
            print(ex)
            raise ValueError("Error al registrar la habitación") from ex

        finally:
            if cursor:
                cursor.close()

    #funcion de control para proteccion de la base de datos y evitar eliminaciones o ediciones a las habitaciones reservadas.
    @classmethod
    def verificar_estado(cls, db, id_habitacion):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = "SELECT estado FROM habitaciones WHERE id_habitacion = %s"

            cursor.execute(sql, (id_habitacion, ))
            row = cursor.fetchone()

            if row is not None:
                return row[0] 
            return None

        except Exception as ex:
            print(f"Error al verificar el estado de la habitación: {ex}")
            raise ValueError("Error al verificar disponibilidad del código") from ex

        finally:
            if cursor:
                cursor.close()
#Funcion Principal
    @classmethod
    def Eliminar_habitacion(cls, db, id_habitacion):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM habitaciones WHERE id_habitacion = %s"
            cursor.execute(sql, (id_habitacion,))
            db.connection.commit()
            return cursor.rowcount > 0

        except Exception as eliminar_habitacion:
            print(eliminar_habitacion)
            raise ValueError("Error al eliminar la habitación") from eliminar_habitacion

        finally:
            if cursor:
                cursor.close()

    #funcion para mostrar de manera precisa  en los labels con jinja2 de la habitacion que se va a editar, OJO no es la que ejecuta la edicion
    #simplemente muestra los datos de la habitacion a editar.
    @classmethod
    def Elementos_habitacion(cls, db, id_habitacion) -> list:
        cursor = None

        try:
            cursor = db.connection.cursor()
            sql = """SELECT tipo, descripcion, capacidad, precio, grado
                    FROM habitaciones WHERE id_habitacion = %s """
            cursor.execute(sql, (id_habitacion,))
            fila = cursor.fetchone()

            if fila:
                habitacion_exacta = {
                        "tipo": fila[0],
                        "descripcion": fila[1],
                        "capacidad": fila[2],
                        "precio": fila[3],
                        "grado": fila[4]
                    }
                return habitacion_exacta

            return None

        except Exception as ex:
            raise ValueError(f"Error al obtener info de la habitacion para editar, Funcion de control {ex}")

        finally:
            if cursor:
                cursor.close()

#Funcion principal Editar
    @classmethod
    def editar_habitacion(cls, db, tipo, grado, capacidad, precio, descripcion, id_habitacion):
        cursor = None

        try:
            cursor = db.connection.cursor()
            sql = """UPDATE habitaciones SET
                tipo = %s,
                grado = %s,
                capacidad = %s,
                precio = %s,
                descripcion = %s
                WHERE id_habitacion = %s"""
            cursor.execute(sql,(tipo, grado, capacidad, precio, descripcion, id_habitacion,))
            db.connection.commit()

            return cursor.rowcount > 0

        except Exception as actualizar_habitacion:
            raise ValueError(f"Error de actualizacion de estados de habitaciones {actualizar_habitacion}")
            
        finally:
            if cursor:
                cursor.close()