from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/usuario/<name>")#ruta personalizada
def saludo(name):
    return f"Bienvenido, {name}"

#Creando Rutas 
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():   
    return render_template("about.html")      
@app.route("/register")
def register():   
    return render_template("auth/register.html")      


































if __name__ == '__main__':
    app.run(debug=True)