from flask import Blueprint, render_template, jsonify, redirect, request, flash, url_for
from conexion.conexion import get_db_connection
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import Usuario 

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route("/dashboard")
@login_required  # Proteger el dashboard
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
        000
        #verificar credenciales 
        user = Usuario.verificar_credenciales(email, password)
        if user: 
            login_user(user)
            flash('inicio de sesion exitoso', 'success')
            print('se inicio sesion correctamente')
            #redirigir a la pagina que se quiera acceder 
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('auth.dashboard'))  
            
        else:
            flash('Las credenciales no son correctas', 'error')  
            print('credenciales no correctas')
            
    
   
    return render_template('auth/login.html')








@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password'] 
        conf_password = request.form['conf_passwordss'] 

        # Verificar si las contraseñas coinciden
        if password != conf_password:
            msj = 'Las contraseñas no coinciden'
            flash(msj)
            
            return render_template('auth/register.html')

        # Verificar si ya existe un usuario con ese correo
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo ya está en uso, intenta con otro', 'error')
            return render_template('auth/register.html')

        # Crear usuario (solo si no existe)
        if Usuario.crear_usuario(username, email, password):
            flash('Cuenta creada con éxito, ya puedes iniciar sesión', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Error al crear la cuenta', 'error')

    return render_template('auth/register.html')
 

@auth.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')

    return redirect(url_for('auth.login'))



#testeat que la DB funcioen de manera correcta 
@auth.route('/test_db')
def test_db():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"status": "error", "message": "No se pudo establecer conexion con la base de datos"}), 500
    try:
        conn.close()
        return jsonify({"status": "success", "message": "Conexion exitosa con la base de datos"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"No se pudo establecer conexion con la base de datos {e}"}), 500