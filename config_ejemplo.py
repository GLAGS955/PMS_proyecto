#Este es un archivo muy importante para que la app funciona aca esta la plantilla para rellenar con sus propias crendenciales

class Config:
    SECRET_KEY = 'aca va tu llave secreta que se usara para mensajes flash y seguridad'

class DevelopmentConfig(Config): #esta clase recibe a la clase Config y tiene la conexion a base de datos
    DEBUG = True
    MYSQL_HOST = 'host de tu base de datos' #Si es local el host simplemente es localhost
    MYSQL_USER = 'tu usuario'
    MYSQL_PASSWORD = 'tu password si tienes, sino dejalo vacio'
    MYSQL_DB = 'nombre de la base de datos'

#Diccionario que se importara en la app.py
config = {
    'Development': DevelopmentConfig
}