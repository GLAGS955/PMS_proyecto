from flask import Blueprint, render_template, redirect, request , url_for, flash, session
from utils.security import login_requerido, es_usted_admin


#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.Entidades.user import User
from database.db import db
from database.modelHabitaciones import ModelHabitaciones
#Configurar el blueprint auth
rutas_sbar = Blueprint('rutas_sbar',__name__)

@rutas_sbar.route('/panel_control', methods = ['GET'])
@login_requerido
@es_usted_admin
def panel_control():
    return render_template('Inicios/vistas_admin/panel_control.html')


rutas_sbar.route('/bienvenidad')
@login_requerido
def bienvenida():
    return render_template('Especial/Bienvenida.html')