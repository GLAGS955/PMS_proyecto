#flask y demas modulos.
from flask import Flask, render_template, url_for, redirect
from config import config

#Seguridad
from utils.security import login_requerido, es_usted_admin
from flask_wtf.csrf import CSRFProtect

#Base de datos
from database.db import db

#Inicializaciones de la app
app_ing = Flask(__name__)

#Configuraciones basicas de config.py
app_ing.config.from_object(config['Development'])
#csfr
csrf = CSRFProtect()
csrf.init_app(app_ing)
#Conexion de base de datos
db.init_app(app_ing)

#                                           REGISTROS DE BLUEPRINTS
from controladores.auth import auth
from controladores.acciones_usuarios import acciones_usuarios
from controladores.cambiar_pwd import cambiar_contraseña
from controladores.rutas_sbar import rutas_sbar
app_ing.register_blueprint(auth)
app_ing.register_blueprint(acciones_usuarios)
app_ing.register_blueprint(cambiar_contraseña)
app_ing.register_blueprint(rutas_sbar)

#                                            Controladores principales
@app_ing.route("/")
def Index():
    return redirect(url_for('auth.login'))

@app_ing.route("/Inicio")
@login_requerido
@es_usted_admin
def Inicio_admin():
    return render_template("Inicios/sbar_admin.html")

@app_ing.route("/clientes")
@login_requerido
def Inicio_clientes():
    return render_template("Inicios/sbar_clientes.html")


@app_ing.route("/operaciones")
@login_requerido
def serve_operaciones():
    return render_template("Opers/Operaciones.html")


@app_ing.route("/contactanos")
@login_requerido
def contactanos():
    return render_template("contactanos.html")


#Manejo de Errores [ 401 / 403 / 404 / 405 / 500 ]
@app_ing.errorhandler(404)
def pagina_no_encontrada(_error):
    return render_template('Errors/Error404.html'), 404


#Configuraciones de errores
app_ing.register_error_handler(404, pagina_no_encontrada)

def correr_app():
    if __name__=='__main__':
        app_ing.run()

correr_app()
