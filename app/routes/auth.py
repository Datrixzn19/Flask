from flask import Blueprint, render_template, jsonify, redirect, request, flash, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from conexion.conexion import get_db_connection
from app.models.user import UsuarioDB

auth = Blueprint('auth', __name__, url_prefix='/auth')


# Dashboard
@auth.route("/dashboard")
@login_required
def dashboard():
    print("Entrada al dashboard")
    return render_template("auth/dashboard.html")


# Login 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Si ya está autenticado, redirige directamente al dashboard
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        # Verificar credenciales
        user = UsuarioDB.verificar_credenciales(email, password)
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            print('Se inició sesión correctamente')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
        else:
            flash('Las credenciales no son correctas', 'danger') 
            print('Credenciales no correctas')
    
    return render_template('auth/login.html')


# resgister
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email'].strip().lower()
        password = request.form['password'] 
        conf_password = request.form.get('conf_password') 

        # Validar contraseñas coincidan
        if password != conf_password:
            flash('Las contraseñas no coinciden', 'warning')
            return render_template('auth/register.html')

        # Verificar si ya existe un usuario con ese correo
        if UsuarioDB.verificar_email_existente(email):
            flash('El correo ya está en uso, intenta con otro', 'warning')
            return render_template('auth/register.html')

        # Crear usuario , solo si no existe
        if UsuarioDB.crear_usuario(username, email, password):
            flash('Cuenta creada con éxito, ya puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al crear la cuenta', 'danger')

    return render_template('auth/register.html')


# cerrar sesion 
@auth.route('/logout')
@login_required
def logout():
    session.pop('_flashes', None)
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))


#testear la db
@auth.route('/test_db')
def test_db():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "No se pudo establecer conexión con la base de datos"}), 500
    
    try:
        conn.close()
        return jsonify({"status": "success", "message": "Conexión exitosa con la base de datos"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"No se pudo cerrar la conexión: {e}"}), 500
