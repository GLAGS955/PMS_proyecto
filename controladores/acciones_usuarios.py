from flask import Blueprint, render_template, redirect, request , url_for, flash, session
from utils.security import login_requerido

#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.Entidades.user import User
from database.db import db

#Configurar el blueprint auth
acciones_usuarios = Blueprint('acciones_usuarios',__name__)

@acciones_usuarios.route('/ver_perfil')
@login_requerido
def perfil_usuario():
    return render_template('common/perfilusuario.html')

@acciones_usuarios.route('/editar_perfil', methods=['GET','POST'])
@login_requerido
def editar_perfil():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        sexo = request.form.get('sexo')
        correo = session['correo']
        ModelUser.actualizar_perfil(db, correo, nombre, sexo)
        flash("¡Tu perfil ha sido actualizado correctamente!")
        return render_template('common/perfilusuario.html')

    return render_template('common/editarperfil.html')