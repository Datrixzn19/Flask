from flask import render_template, Blueprint, jsonify
from conexion.conexion import get_db_conection #importanmos la funcion buscando en la carpeta.archivo.py  para conectar a mysql



main = Blueprint('main', __name__)

@main.route("/usuario/<name>")#ruta personalizada
def saludo(name):
    return f"Bienvenido, {name}"






#Creando Rutas 
@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/about")
def about():   
    return render_template("main/about.html")      





@main.route('/test_db')
def test_db():

    conn = get_db_conection()#llamamnos la funcion
    
    if conn is None:
        return jsonify({"status": "error", "messaje": "No se pudo establecer conexion con la base de datos"}), 500
    try:
        conn.close()#si la conexion fue exitosa la cerramos
        return jsonify({"status": "success", "messaje": "Conexion exitosa con la base de datos"})
    except Exception as e:
        return jsonify({"status": "error", "messaje": f"No se pudo establecer conexion con la base de datos {e}"}), 500





