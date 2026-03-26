from functools import wraps
from flask import session, url_for, redirect, flash

# CENTINELAS PARA LAS VISTAS

def login_requerido(funcion):
    @wraps(funcion)
    def funcion_especial(*args,**kwargs):
        if "nombre" not in session:
            flash('Por favor, inicia sesión para acceder.')
            return redirect(url_for('auth.login'))
        return funcion(*args,**kwargs)
    return funcion_especial

def es_usted_admin(admin):
    @wraps(admin)

    def Rol(*args, **kwargs):
        rol = session.get("rol")

        if rol != "admin":
            flash("Acesso Denegado")
            return redirect(url_for('Inicio_clientes'))
        return admin(*args, **kwargs)
    return Rol



