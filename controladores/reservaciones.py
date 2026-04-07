from flask import Blueprint, render_template, redirect, request , url_for, flash, session
from utils.security import login_requerido, es_usted_admin


#Conexion de base de datos y modelos del blueprints auth
from database.modelUser import ModelUser
from database.db import db


#Configurar el blueprint auth
reservaciones = Blueprint('reservaciones',__name__)