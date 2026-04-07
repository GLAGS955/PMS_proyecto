from flask import Blueprint, render_template, redirect, request , url_for, flash, session
from utils.security import login_requerido, es_usted_admin


#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.Entidades.habitaciones import Habitaciones
from database.db import db
from database.modelHabitaciones import ModelHabitaciones

#Configurar el blueprint auth
habitaciones = Blueprint('habitaciones',__name__)


@habitaciones.route('/habitaciones', methods = ['GET'])
@login_requerido

def listar_habitaciones():
    lista_habitaciones = ModelHabitaciones.Obtener_habitaciones(db)
    return render_template('common/LogicaNegocios/VistasHabitaciones/habitaciones.html', habitaciones=lista_habitaciones)

@habitaciones.route('/añadir_habitacion', methods = ['GET', 'POST'])
@login_requerido
@es_usted_admin

def agregar_habitacion():
    if request.method == 'POST':

        foto = request.form.get('foto')
        foto_optimizada = foto.strip()
        estado = "Disponible"
        codigo = request.form.get('codigo')
        #Filtros de limpieza de datos
        #Los datos de html por defecto vienen en str y nuestra base de datos tienen campos estrictos de tipos de datos xd
        capacidad_cruda_form = request.form.get('capacidad')
        capacidad_filtrada = int(capacidad_cruda_form)

        precio_form = request.form.get('precio')
        precio_filtrado = float(precio_form)

        nueva_habitacion = (
            codigo,
            request.form.get('tipo'),
            request.form.get('descripcion'),
            estado,
            capacidad_filtrada,
            precio_filtrado,
            request.form.get('grado'),
            foto_optimizada
        )
        if ModelHabitaciones.verificar_codigo(db,codigo):
            flash(f"Ohh, lo sentimos el codigo {codigo} no esta disponible")
            return redirect(url_for('habitaciones.agregar_habitacion'))

        else:
            ModelHabitaciones.agregar_habitacion(db,nueva_habitacion)
            flash(f"¡La habitacion numero {codigo} fue agregada exitosamente! ", "success")
            return redirect(url_for('habitaciones.listar_habitaciones'))

    return render_template('common/LogicaNegocios/VistasHabitaciones/agregar.html')

@habitaciones.route('/editar_habitacion/<int:id_exacto>', methods = ['GET', 'POST'])
@login_requerido
@es_usted_admin
def editar_habitacion(id_exacto):
    estado = ModelHabitaciones.verificar_estado(db,id_exacto)

    if estado in ['Ocupada','Pendiente']:
        flash("¡Espera esta habitacion no se puede editar porque esta reservada!")
        return redirect(url_for('habitaciones.listar_habitaciones'))

    #primer paso para la edicion mostrar datos de la habitacion a editar
    habitacion_exacta = ModelHabitaciones.Elementos_habitacion(db,id_exacto)
    return render_template ('common/LogicaNegocios/vistasHabitaciones/editarhabitacion.html', habitacion = habitacion_exacta, id_habitacion = id_exacto)


@habitaciones.route('/eliminar_habitacion/<int:id_exacto>', methods = ['POST'])
@login_requerido
@es_usted_admin
def eliminar_habitacion(id_exacto):

    estado = ModelHabitaciones.verificar_estado(db,id_exacto)

    if estado in ['Ocupada','Pendiente']:
        flash("¡Espera esta habitacion no se puede eliminar porque esta reservada!")
        return redirect(url_for('habitaciones.listar_habitaciones'))

    else:
        ModelHabitaciones.Eliminar_habitacion(db,id_exacto)
        flash("¡La habitacion fue eliminada correctamente!")
        return redirect(url_for('habitaciones.listar_habitaciones'))
