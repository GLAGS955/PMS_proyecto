class ModelPagos:

    @classmethod
    def obtener_factura_exacta(cls, db, id_reserva):
        cursor = None
        try:
            cursor = db.connection.cursor()
        
            sql = """SELECT r.id_reservacion, c.nombre, c.cedula, h.codigo, h.precio, h.estado,
                            r.fecha_hora_checkin, r.fecha_hora_checkout, r.tiempo_dias,
                            (SELECT id_pago FROM pagos WHERE id_reservacion = r.id_reservacion LIMIT 1) as pagado
                        FROM reservaciones r
                        JOIN clientes c ON r.id_cliente = c.id_cliente
                        JOIN habitaciones h ON r.id_habitacion = h.id_habitacion
                        WHERE r.id_reservacion = %s"""
            cursor.execute(sql, (id_reserva,))
            fila = cursor.fetchone()
            
            if fila:
                return {
                    "id_reservacion": fila[0], "cliente": fila[1], "cedula": fila[2],
                    "hab_codigo": fila[3], "precio_bruto": fila[4], "estado_hab": fila[5],
                    "checkin": fila[6], "checkout": fila[7], "dias": fila[8],
                    "esta_pagado": True if fila[9] else False
                }
            return None
        finally:
            if cursor: cursor.close()

    @classmethod
    def registrar_pago_express(cls, db, id_reserva, metodo):
        cursor = None
        try:
            cursor = db.connection.cursor()
            sql = "INSERT INTO pagos (monto, metodo_pago, fecha_pago, id_reservacion, id_usuario) VALUES (0, %s, NOW(), %s, 1)"
            cursor.execute(sql, (metodo, id_reserva))
            db.connection.commit()
            return True
        finally:
            if cursor: cursor.close()