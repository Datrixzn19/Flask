from flask import Flask 


app = Flask(__name__)

@app.route("/")#esta es la ruta base 
def index():
    return "Esta es la pagina principal "

@app.route("/usuario/<name>")#ruta personalizada
def saludo(name):
    return f"Bienvenido, {name}"


if __name__ == '__main__':
    app.run(debug=True)