from flask import Blueprint, request, jsonify, session, flash, render_template
# Base de datos y consultas sql
from database.modelUser import ModelUser
from database.db import db

# Nuestro modulo para esta parte es una api rest sencilla 
cambiar_contraseña = Blueprint('cambiar_contraseña', __name__)


@cambiar_contraseña.route('/recuperar_contraseña')
def vista_recuperar():
    return render_template('Auth/recuperar.html')


@cambiar_contraseña.route('/api/validar-usuario', methods=['POST'])
def validar_usuario():
    datos = request.get_json()
    correo = datos.get('correo')
    
    correo_filtrado = ModelUser.verificar_correo(db, correo)

    if correo_filtrado:
        session['correo_en_recuperacion'] = correo
        return jsonify({"mensaje": "Usuario encontrado"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404



@cambiar_contraseña.route('/api/validar-pista', methods=['POST'])
def validar_pista():
    datos = request.get_json()
    pista_ingresada = datos.get('pista')

    correo_actual = session.get('correo_en_recuperacion')

    if not correo_actual:
        return jsonify({"error": "Sesión expirada"}), 400


    pista_correcta = ModelUser.verificar_pista(db, correo_actual, pista_ingresada)

    if pista_correcta:
        session['pista_aprobada'] = True
        return jsonify({"mensaje": "Pista correcta"}), 200
    else:
        return jsonify({"error": "Pista incorrecta"}), 401


@cambiar_contraseña.route('/api/cambiar-pwd', methods=['POST'])
def cambiar_pwd():
    if not session.get('pista_aprobada') or not session.get('correo_en_recuperacion'):
        return jsonify({"Sospechoso": "No tienes permiso para hacer esto"}), 403

    datos = request.get_json()
    nueva_pwd = datos.get('nueva_pwd')
    correo_actual = session.get('correo_en_recuperacion')

    ModelUser.actualizar_pwd(db, correo_actual, nueva_pwd)


    session.pop('correo_en_recuperacion', None)
    session.pop('pista_aprobada', None)


    flash("La contraseña ha sido cambiada exitosamente", "success")

    return jsonify({"mensaje": "Contraseña actualizada"}), 200