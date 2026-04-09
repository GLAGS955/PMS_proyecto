from flask import Blueprint, render_template, redirect, request , url_for, flash, session
from utils.security import login_requerido, es_usted_admin


#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.db import db
from database.modelClientes import ModelClientes

#Configurar el blueprint auth
clientes = Blueprint('clientes',__name__)

@clientes.route('/ver_clientes', methods=['GET'])
@login_requerido
@es_usted_admin
def listar_clientes():

    lista_clientes = ModelClientes.Obtener_clientes(db)
    return render_template('common/LogicaNegocios/Clientes/ver_clientes.html', clientes=lista_clientes)

@clientes.route('/agregar', methods=['GET', 'POST'])
@login_requerido
def agregar_cliente():
    # 1. Atrapamos el id_habitacion de la URL (si viene del proceso de reserva online)
    id_habitacion = request.args.get('id_habitacion')

    if request.method == 'POST':

        cedula_limpia = request.form.get('cedula').strip()
        nombre_limpio = request.form.get('nombre').strip()

        nuevo_cliente = (
            nombre_limpio,
            cedula_limpia
        )

        if ModelClientes.verificar_cedula(db, cedula_limpia):
            flash(f"Ohh, lo sentimos. La cédula {cedula_limpia} ya está registrada en el sistema.")
            # Si hay error, recargamos la página pero conservamos el id_habitacion en la URL
            return redirect(url_for('clientes.agregar_cliente', id_habitacion=id_habitacion))

        else:
            ModelClientes.agregar_cliente(db, nuevo_cliente)
            flash(f"¡El cliente {nombre_limpio} fue registrado exitosamente!", "success")
            
            # ==========================================
            # LA MAGIA DEL IF: SEPARACIÓN DE CAMINOS
            # ==========================================
            if session.get('rol') == 'admin':
                # El admin vuelve a su tabla de directorio
                return redirect(url_for('clientes.listar_clientes'))
            else:
                # El cliente sigue su camino hacia el checkout prellenado
                return redirect(url_for('reservaciones.agregar_reservacion', id_habitacion=id_habitacion))
    # GET: Pasamos el id_habitacion a la vista por si lo necesita el HTML
    return render_template('common/LogicaNegocios/Clientes/registrar_cliente.html', id_habitacion=id_habitacion)

@clientes.route('/mostrar_cliente_exacto/<int:id_exacto>', methods = ['GET', 'POST'])
@login_requerido
@es_usted_admin
def ver_cliente(id_exacto):
    
    # Obtenemos los datos para el autollenado
    cliente_exacto = ModelClientes.Elementos_cliente(db, id_exacto)
    
    return render_template('common/LogicaNegocios/Clientes/editar_cliente.html', cliente=cliente_exacto, id_cliente=id_exacto)


@clientes.route('/editar_cliente/<int:id_exacto>', methods = ['GET', 'POST'])
@login_requerido
@es_usted_admin
def editar_cliente(id_exacto):
    
    if request.method == 'POST':

        nombre = request.form.get('nombre')
        cedula = request.form.get('cedula')

        # Pasamos los datos al modelo
        if ModelClientes.editar_cliente(db, nombre, cedula, id_exacto):
            flash("¡El cliente fue actualizado correctamente!")
            return redirect(url_for('clientes.listar_clientes'))
        
        else:
            flash("¡Oh, la actualizacion del cliente ha fracasado o no hubo cambios, vuelve a intentarlo!")
            return redirect(url_for('clientes.listar_clientes'))
        

@clientes.route('/eres_cliente')
def eres_cliente():

    id_hab = request.args.get('id_habitacion')
    return render_template('common/LogicaNegocios/Clientes/eres_cliente.html', id_habitacion=id_hab)