from flask import render_template, Blueprint


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



