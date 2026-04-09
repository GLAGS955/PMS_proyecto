class ModelClientes:

    @classmethod
    def agregar_cliente(cls, db, nuevo_cliente):
        cursor = None
        try:
            cursor = db.connection.cursor()
            # La tabla solo pide nombre y cédula (el id_cliente es automático)
            sql = """INSERT INTO clientes (nombre, cedula)
                        VALUES (%s, %s)"""
            
            cursor.execute(sql, nuevo_cliente)
            db.connection.commit()
            return True

        except Exception as ex:
            print(ex)
            raise ValueError("Error al registrar el cliente") from ex

        finally:
            if cursor:
                cursor.close()

    @classmethod
    def verificar_cedula(cls, db, cedula):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_cliente FROM clientes WHERE cedula = %s"
            cursor.execute(sql, (cedula,))
            return cursor.fetchone() is not None
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def Obtener_clientes(cls, db) -> list:
        cursor = None

        try:
            cursor = db.connection.cursor()
            # Solo traemos los 3 campos solicitados
            sql = "SELECT id_cliente, nombre, cedula FROM clientes"
            cursor.execute(sql)
            filas = cursor.fetchall()

            clientes = []

            for fila in filas:
                clientes.append({
                    "id_cliente": fila[0],
                    "nombre": fila[1],
                    "cedula": fila[2]
                })
            return clientes

        except Exception as ex:
            raise ValueError(f"Error al obtener la lista de clientes: {ex}")
        finally:
            if cursor:
                cursor.close()


    @classmethod
    def Elementos_cliente(cls, db, id_cliente) -> dict:
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """SELECT nombre, cedula
                    FROM clientes WHERE id_cliente = %s """
            cursor.execute(sql, (id_cliente,))
            fila = cursor.fetchone()

            if fila:
                cliente_exacto = {
                    "nombre": fila[0],
                    "cedula": fila[1]
                }
                return cliente_exacto
            return None

        except Exception as ex:
            raise ValueError(f"Error al obtener info del cliente para editar, Funcion de control {ex}")

        finally:
            if cursor:
                cursor.close()


    @classmethod
    def editar_cliente(cls, db, nombre, cedula, id_cliente):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE clientes SET
                    nombre = %s,
                    cedula = %s
                    WHERE id_cliente = %s"""
            cursor.execute(sql, (nombre, cedula, id_cliente,))
            db.connection.commit()

            return cursor.rowcount > 0

        except Exception as actualizar_cliente:
            raise ValueError(f"Error de actualizacion de clientes {actualizar_cliente}")
            
        finally:
            if cursor:
                cursor.close()