from flask_login import UserMixin
from conexion.conexion import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioDB(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

    # Verificar si el correo ya existe
    @staticmethod
    def verificar_email_existente(email):
        email = email.strip().lower()
        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error al verificar email: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # Crear un nuevo usuario
    @staticmethod
    def crear_usuario(nombre, email, password):
        email = email.strip().lower()
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if not conn:
            return False
        cursor = conn.cursor(dictionary=True)
        try:
            # Verificar si ya existe el correo
            query_check = "SELECT id FROM usuarios WHERE email = %s"
            cursor.execute(query_check, (email,))
            if cursor.fetchone():
                print("El correo ya existe")
                return False

            # Insertar nuevo usuario
            query_insert = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query_insert, (nombre, email, hashed_password))
            conn.commit()
            return True
        except Exception as ex:
            print(f"Error al crear usuario: {ex}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    # Verificar credenciales
    @staticmethod
    def verificar_credenciales(email, password):
        email = (email or "").strip().lower()
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT id, nombre, email, password FROM usuarios WHERE email = %s"
            cursor.execute(query, (email,))
            user_data = cursor.fetchone()
            if user_data and check_password_hash(user_data['password'], password):
                return UsuarioDB(user_data['id'], user_data['nombre'], user_data['email'])
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
        finally:
            cursor.close()
            conn.close()
        return None

    # Obtener usuario por id (para Flask-Login)
    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return UsuarioDB(user_data['id'], user_data['nombre'], user_data['email'])
        except Exception as ex:
            print(f"Error al encontrar user por id: {ex}")
        finally:
            cursor.close()
            conn.close()
        return None
