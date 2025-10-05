from flask import Blueprint, render_template, jsonify, redirect, request, flash, url_for
from conexion.conexion import get_db_connection
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import UsuarioDB

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/dashboard")
@login_required
def dashboard():
    print("entrada al dashboard")
    return render_template("auth/dashboard.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
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

            # Redirigir a la página deseada
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))
        else:
            flash('Las credenciales no son correctas', 'error')  
            print('Credenciales no correctas')
    
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email'].strip().lower()
        password = request.form['password'] 
     
        # Verificar si ya existe un usuario con ese correo
        if UsuarioDB.verificar_email_existente(email):
            flash('El correo ya está en uso, intenta con otro', 'error')
            return render_template('auth/register.html')

        # Crear usuario (solo si no existe)
        if UsuarioDB.crear_usuario(username, email, password):
            flash('Cuenta creada con éxito, ya puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al crear la cuenta', 'error')

    return render_template('auth/register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))


# Test para verificar que la DB funciona correctamente
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
