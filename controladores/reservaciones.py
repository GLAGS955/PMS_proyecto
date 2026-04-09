from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from utils.security import login_requerido, es_usted_admin
from database.db import db
from database.modelReservaciones import ModelReservaciones
from database.modelClientes import ModelClientes
from database.modelHabitaciones import ModelHabitaciones

reservaciones = Blueprint('reservaciones', __name__)

@reservaciones.route('/nueva', methods=['GET', 'POST'])
@login_requerido
def agregar_reservacion():

    if request.method == 'POST':
        
        id_cliente = request.form.get('id_cliente') if session.get('rol') == 'admin' else session.get('id_cliente', 1) 
        
        id_habitacion = request.form.get('id_habitacion')
        checkin_str = request.form.get('checkin')
        checkout_str = request.form.get('checkout')
        descripcion = "Reserva en Plataforma"

        # Cálculo de días
        try:
            formato = "%Y-%m-%d"
            fecha_in = datetime.strptime(checkin_str, formato)
            fecha_out = datetime.strptime(checkout_str, formato)
            tiempo_dias = (fecha_out - fecha_in).days
            if tiempo_dias <= 0: tiempo_dias = 1
        except:
            tiempo_dias = 1

        
        datos = (tiempo_dias, descripcion, id_cliente, id_habitacion, checkin_str, checkout_str)
        id_nueva_reserva = ModelReservaciones.agregar_reservacion(db, datos)
        
        flash("¡Reserva confirmada exitosamente! Generando factura...", "success")
        
        
        return redirect(url_for('pagos.ver_factura', id_reserva=id_nueva_reserva))

    
    id_habitacion_pre = request.args.get('id_habitacion')
    habitacion_seleccionada = None

    clientes = ModelClientes.Obtener_clientes(db)
    lista_habitaciones = ModelHabitaciones.Obtener_habitaciones(db)

    # Buscamos la habitación que coincida con la URL
    if id_habitacion_pre:
        for hab in lista_habitaciones:
            if str(hab['id_habitacion']) == str(id_habitacion_pre):
                habitacion_seleccionada = hab
                break

    
    return render_template('common/LogicaNegocios/VistasReservaciones/reservaciones.html', 
                            clientes=clientes, 
                            habitaciones=lista_habitaciones,
                            habitacion_pre=habitacion_seleccionada)


@reservaciones.route('/lista', methods=['GET'])
@login_requerido
@es_usted_admin
def listar_reservaciones():
    lista = ModelReservaciones.listar_reservaciones(db)
    return render_template('common/LogicaNegocios/vistasReservaciones/ver_reservas.html', reservas=lista)




@reservaciones.route('/checkin/<int:id_reserva>')
@login_requerido
@es_usted_admin
def hacer_checkin(id_reserva):
    try:
        # Cambiamos el estado de la habitación a "Ocupada"
        ModelReservaciones.cambiar_estado_por_reserva(db, id_reserva, 'Ocupada')
        flash('¡Check-In exitoso! La habitación ahora está Ocupada.', 'success')
    except Exception as e:
        flash(f'Error en el Check-In: {e}', 'danger')
        
    return redirect(url_for('reservaciones.listar_reservaciones'))

@reservaciones.route('/checkout/<int:id_reserva>')
@login_requerido
@es_usted_admin
def hacer_checkout(id_reserva):
    try:
        
        ModelReservaciones.cambiar_estado_por_reserva(db, id_reserva, 'Disponible')
        flash('¡Check-Out exitoso! La habitación vuelve a estar Disponible.', 'success')
    except Exception as e:
        flash(f'Error en el Check-Out: {e}', 'danger')
        
    return redirect(url_for('reservaciones.listar_reservaciones'))