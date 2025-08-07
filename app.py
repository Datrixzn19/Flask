from flask import Flask, render_template, url_for 
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("auth/register.html")

@app.route("/prices")
def prices():
    return render_template("prices.html")
