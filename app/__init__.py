from flask import Flask
import os
from dotenv import load_dotenv
from .db.models import init_db



# Cargar variables de entorno
load_dotenv()

# Importar blueprints
from .routes.main import main
from .routes.auth import auth
from .products.routes import products_bp   # sqlite

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "dev")
   

    # Configuración de la base de datos
    app.config["DATABASE"] = os.path.join(app.instance_path, "database.db")
    os.makedirs(app.instance_path, exist_ok=True)  

    # Inicializar DB
    init_db(app)

    # Registrar blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(products_bp, url_prefix="/products")  # 











    return app
