#conectarse a mysql
#pip install mysql-connector-python
import mysql.connector

#configurar datos de conexion
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'proyecto_desarrollo_web',
}

def get_db_conection():
    try:
        #intentara la coneccion con los datos de db_config
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f'Ha ocurrido un error al intentar la conexion a la DB --> {err}')
        return None 