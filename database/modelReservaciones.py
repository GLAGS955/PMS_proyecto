from datetime import datetime
class ModelReservaciones:

    @classmethod
    def verificar_disponibilidad(cls, db, id_habitacion, checkin, checkout):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_reservacion FROM reservaciones 
                        WHERE id_habitacion = %s 
                        AND fecha_hora_checkin < %s 
                        AND fecha_hora_checkout > %s"""
            
            cursor.execute(sql, (id_habitacion, checkout, checkin))
            return cursor.fetchone() is None 
            
        except Exception as ex:
            raise ValueError(f"Error al verificar fechas: {ex}")
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def agregar_reservacion(cls, db, datos_reserva):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql_insert = """INSERT INTO reservaciones 
                        (tiempo_dias, descripcion, id_cliente, id_habitacion, fecha_hora_checkin, fecha_hora_checkout)
                        VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert, datos_reserva)
            id_nueva = cursor.lastrowid

            id_hab = datos_reserva[3]
            sql_update = "UPDATE habitaciones SET estado = 'Pendiente' WHERE id_habitacion = %s"
            cursor.execute(sql_update, (id_hab,))

            db.connection.commit()
            return id_nueva 
        except Exception as ex:
            print(ex)
            raise ValueError("Error al registrar la reserva") from ex
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def listar_reservaciones(cls, db):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """SELECT r.id_reservacion, c.nombre, h.codigo, h.estado, 
                            r.fecha_hora_checkin, r.fecha_hora_checkout, r.tiempo_dias 
                    FROM reservaciones r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
                    ORDER BY r.fecha_hora_checkin DESC"""
            
            cursor.execute(sql)
            filas = cursor.fetchall()

            reservas = []

            for fila in filas:
                reservas.append({
                    "id_reservacion": fila[0],
                    "nombre": fila[1],
                    "codigo": fila[2],
                    "estado_habitacion": fila[3],  
                    "fecha_hora_checkin": fila[4],
                    "fecha_hora_checkout": fila[5],
                    "tiempo_dias": fila[6]
                })
                
            return reservas
            
        except Exception as ex:
            raise ValueError(f"Error al listar las reservaciones: {ex}")
            
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def cambiar_estado_por_reserva(cls, db, id_reservacion, nuevo_estado):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE habitaciones h
                    JOIN reservaciones r ON h.id_habitacion = r.id_habitacion
                    SET h.estado = %s
                    WHERE r.id_reservacion = %s"""

            cursor.execute(sql, (nuevo_estado, id_reservacion))
            db.connection.commit()
            return True

        except Exception as ex:
            raise ValueError(f"Error al cambiar el estado de la habitación: {ex}")
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def obtener_resumen_hoy(cls, db):
        cursor = None
        try:
            cursor = db.connection.cursor()
            hoy = datetime.now().strftime('%Y-%m-%d')

            cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE estado = 'Disponible'")
            hab_disp = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE estado = 'Ocupada'")
            hab_ocup = cursor.fetchone()[0]

            cursor.execute("""SELECT COUNT(*) FROM reservaciones r 
                                JOIN habitaciones h ON r.id_habitacion = h.id_habitacion 
                                WHERE DATE(r.fecha_hora_checkin) = %s AND h.estado = 'Pendiente'""", (hoy,))
            checkins_hoy = cursor.fetchone()[0]

            cursor.execute("""SELECT COUNT(*) FROM reservaciones r 
                                JOIN habitaciones h ON r.id_habitacion = h.id_habitacion 
                                WHERE DATE(r.fecha_hora_checkout) = %s AND h.estado = 'Ocupada'""", (hoy,))
            checkouts_hoy = cursor.fetchone()[0]

            sql_llegadas = """
                SELECT c.nombre, c.cedula, h.codigo, h.tipo, r.tiempo_dias, r.id_reservacion
                FROM reservaciones r
                JOIN clientes c ON r.id_cliente = c.id_cliente
                JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
                WHERE DATE(r.fecha_hora_checkin) = %s AND h.estado = 'Pendiente'
            """
            cursor.execute(sql_llegadas, (hoy,))
            filas_llegadas = cursor.fetchall()
            
            lista_llegadas = []
            for f in filas_llegadas:
                lista_llegadas.append({
                    "nombre": f[0], "cedula": f[1], "codigo": f[2], 
                    "tipo": f[3], "dias": f[4], "id_reserva": f[5]
                })

            return {
                "hab_disponibles": hab_disp,
                "hab_ocupadas": hab_ocup,
                "checkins_hoy": checkins_hoy,
                "checkouts_hoy": checkouts_hoy,
                "tabla_llegadas": lista_llegadas
            }
            
        except Exception as ex:
            raise ValueError(f"Error al cargar el dashboard: {ex}")
        finally:
            if cursor: cursor.close()