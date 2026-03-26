from flask import Blueprint, render_template, redirect, request , url_for, flash, session

#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.Entidades.user import User
from database.db import db

#Configurar el blueprint auth
auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        user = User(0,request.form['correo'],0, request.form['pwd'],0,0,0,0) 

        logged_user = ModelUser.login(db, user)
#Validaciones para el usuario
        if logged_user is not None:

            if logged_user.pwd:
                session['rol'] = logged_user.tipo_rol
                session['correo'] = logged_user.correo
                session['nombre'] = logged_user.nombre
                session['edad'] = logged_user.edad
                session['sexo'] = logged_user.sexo

                if session["rol"] == "admin":
                    return redirect(url_for('Inicio_admin'))
                else:
                    return redirect(url_for('Inicio_clientes'))


            else:
                flash("La contraseña es incorrecta...")
                return render_template("Auth/login.html")
        else:
            flash("¡Ups, usuario no encontrado!")
            return render_template("Auth/login.html")

    return render_template("Auth/login.html")

@auth.route('/registro', methods=['GET','POST'])
def registro():
#Validaciones antes del registro
    if request.method == 'POST':
        edad = int(request.form['edad'])
        correo = request.form['correo']

        if edad < 18:
            flash("No tienes la edad sufuciente para registrarte")
            return render_template('Auth/login.html')
        
        if ModelUser.verificar_correo(db, correo):
            flash("Este correo ya esta registrado")
            return render_template('Auth/login.html')
#registro
        else:
            contraseña = User.hashear_pwd(request.form['pwd'])
            pista = User.hashear_pista(request.form['pista'])
            nuevo_usuario = User(
                    0,
                    correo,
                    request.form['nombre'],
                    contraseña,
                    pista,
                    edad,
                    request.form['sexo'],
                    2
        )
            
        if ModelUser.registrar(db, nuevo_usuario):
            flash("¡Registro exitoso!")
            return redirect(url_for('auth.login'))
        else:
            flash("Error interno al registrar!")

    return render_template('Auth/registro.html')


@auth.route('/salir')
def cerrar_session():
    session.clear()
    flash("¡Has cerrado sesion exitosamente!")
    return redirect(url_for('auth.login'))
