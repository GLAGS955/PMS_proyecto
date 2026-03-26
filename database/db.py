""" Aca creamos este archivo para poder usarlo tanto en la app.py como en los blueprints y evitar conflito y la importacion
circular """

from flask_mysqldb import MySQL

db = MySQL()

