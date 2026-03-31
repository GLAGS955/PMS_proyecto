from werkzeug.security import check_password_hash, generate_password_hash

class User():

    def __init__(self, id_usuario, correo, nombre, pwd, pista, edad, sexo, tipo_rol):
        self.id_usuario = id_usuario
        self.correo = correo
        self.nombre = nombre
        self.pwd = pwd
        self.pista = pista
        self.edad = edad
        self.sexo = sexo
        self.tipo_rol = tipo_rol

    #Checkeador universal
    @classmethod
    def check_password(cls, campo_hash, campo_normal):
        return check_password_hash(campo_hash, campo_normal)
    
    #Metodos para el registro de usuarios
    @classmethod
    def hashear_pwd(cls, pwd):
        pwd_hash = generate_password_hash(pwd)
        return pwd_hash
    
    @classmethod
    def hashear_pista(cls, pista):
        pista_hash = generate_password_hash(pista)
        return pista_hash
   

