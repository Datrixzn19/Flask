from flask_login import UserMixin # proporciona metodos hechos para flask login como is_authenticated is_active etc
from conexion.conexion import get_db_connection #mi conexion
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin):
    def __init__(self,id,nombre,email):
        self.id = id
        self.nombre = nombre
        self.email = email

            #CREAR USUARIO 
    @staticmethod #para no necesitar instanciar la clase
    def crear_usuario(nombre, email, password):
        hashed_password = generate_password_hash(password) #mayor seguridad

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                #los % en las consultas son placeholders 
                #reemplaza estos %s con los valores del segundo parametro de execute()
                query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, email, hashed_password))
                conn.commit()
                return True
            except Exception as ex:
                print(f"error al crear usuario {ex}")
                conn.rollback() #deshacer cambios si algo falla 
                return False
            finally:
                cursor.close()
                conn.close()
        return False #en caso de no poder conectarse
           

            #VALIDAR CREDENCIALES 

    @staticmethod
    def verificar_credenciales(email, password):
        # Normalizar email
        email = (email or "").strip().lower()
        conn = get_db_connection()

        if conn:
            cursor = conn.cursor(dictionary=True)
            try:            
                query = "SELECT id, nombre, email, password FROM usuarios WHERE email = %s"  # AQUI CAMBIO
                cursor.execute(query, (email,))
                user_data = cursor.fetchone()
                if user_data and check_password_hash(user_data['password'], password):
                    return Usuario(user_data['id'], user_data['nombre'], user_data['email'])
            except Exception as e:
                print(f"Error al verificar credenciales: {e}")
            finally:
                cursor.close()
                conn.close()
        return None









            #VERIFICAR CREDENCIALES 
    @staticmethod 
    #flask login necesita reconstruir el user cada que se hace una peticion nueva
    #Cuando esta logeado flask-login solo guarda su id, pero necesitamos toda la info
    def get_by_id(user_id):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)#hcae que los resultados sean en diccionario y no es tuplas 
            try:
                #buscar por id
                query = "SELECT * from usuarios WHERE id = %s"
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone() #obtener un solo registro

                # en caso de encontrarlo, cremos y retornamos la instancia 
                if user_data:
                    return Usuario(user_data['id'], user_data['nombre'], user_data['email'])
            except Exception as ex:
                print(f"Error al encontra user por id {ex}") 
            finally:
                cursor.close()
                conn.close()
