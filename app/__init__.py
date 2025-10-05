from flask import Flask
import os
from dotenv import load_dotenv

from flask_login import LoginManager
from app.models.user import UsuarioDB

load_dotenv()

from .routes.main import main
from .routes.auth import auth
from .routes.prods_bp import prods_bp

# Inicializar LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página"

@login_manager.user_loader
def load_user(user_id):
    return UsuarioDB.get_by_id(user_id)

# Crear la app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev")
    app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")
    os.makedirs(app.instance_path, exist_ok=True)

    # Registrar blueprints
    app.register
