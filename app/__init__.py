from flask import Flask 
from .routes.main import main 
from .routes.auth import auth 

import os
from dotenv import load_dotenv

load_dotenv()  # carga el .env en os.environ

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev")  # 'dev' si no encuentra la variable
    print("Secret Key cargada:", app.config['SECRET_KEY']) 
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app
