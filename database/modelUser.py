from .Entidades.user import User

class ModelUser():

    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()

            sql = """
                SELECT u.id_usuario, u.correo, u.nombre, u.pwd, u.pista, u.edad, u.sexo, r.tipo_de_visitante
                FROM usuarios u 
                INNER JOIN roles r ON u.id_rol = r.id_rol
                WHERE u.correo = %s 
            """

            cursor.execute(sql, (user.correo,))
            row = cursor.fetchone()

            if row is not None:

                usuario_validado = User(
                    row[0],
                    row[1],
                    row[2],
                    User.check_password(row[3], user.pwd),
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )

                return usuario_validado
            else:
                return None

        except Exception as ex:
            print(ex)
            raise ValueError("Error de inicio de session") from ex


    @classmethod
    def verificar_correo(cls, db, correo):
        cursor = db.connection.cursor()
        sql = "SELECT id_usuario FROM usuarios WHERE correo = %s"
        cursor.execute(sql, (correo,))
        existe = cursor.fetchone()
        return existe is not None

    @classmethod
    def registrar(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO usuarios (correo, nombre, pwd, pista, edad, sexo, id_rol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            params = (user.correo, user.nombre, user.pwd, user.pista,
                    user.edad, user.sexo, user.tipo_rol)
            cursor.execute(sql, params)
            db.connection.commit()
            return True
        except Exception as ex:
            print(ex)
            raise ValueError("Error de registro") from ex

    @classmethod
    def verificar_pista(cls, db, correo, pista):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT pista FROM usuarios WHERE correo = %s"
            cursor.execute(sql, (correo,))
            row = cursor.fetchone()

            if row is not None:
                pista_hash_guardada = row[0]
                cursor.close()
                return User.check_password(pista_hash_guardada, pista)

            cursor.close()
            return False

        except Exception as ex:
            print(ex)
            raise ValueError("Error de verificar pista") from ex

    @classmethod
    def actualizar_pwd(cls, db, correo, nueva_pwd):
        try:
            cursor = db.connection.cursor()
            hash_nueva_pwd = User.hashear_pwd(nueva_pwd)
            sql = "UPDATE usuarios SET pwd = %s WHERE correo = %s"

            cursor.execute(sql, (hash_nueva_pwd, correo))
            db.connection.commit()

            if cursor.rowcount > 0:
                cursor.close()
                return True
            else:
                cursor.close()
                return False

        except Exception as ex:
            print(ex)
            raise ValueError("Error de actualizar contraseña") from ex
        
    @classmethod
    def actualizar_perfil(cls, db, correo, nuevo_nombre, nuevo_sexo):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE usuarios SET nombre = %s, sexo = %s WHERE correo = %s"

            cursor.execute(sql, (nuevo_nombre,nuevo_sexo, correo))
            db.connection.commit()

            if cursor.rowcount > 0:
                cursor.close()
                return True
            else:
                cursor.close()
                return False

        except Exception as ex:
            print(ex)
            raise ValueError("Error de actualizar perfil") from ex
