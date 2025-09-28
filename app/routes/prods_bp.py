from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from conexion.conexion import get_db_connection
import sys 
import os

# Añadir el directorio raíz al path para importar conexion
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from conexion.conexion import get_db_connection

prods_bp = Blueprint('prods', __name__)

@prods_bp.route('/listar')
def listar():
    conn = get_db_connection()
    if not conn:
        flash('Error de conexión a la base de datos', 'danger')
        return render_template('prods/listar.html', prods=[])
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, c.nombre as categoria_nombre 
            FROM productos p 
            JOIN categorias c ON p.categoria_id = c.id
        """)
        prods = cursor.fetchall()
        return render_template('prods/listar.html', prods=prods)
    except Exception as e:
        flash(f'Error al obtener productos: {str(e)}', 'danger')
        return render_template('prods/listar.html', prods=[])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@prods_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    conn = get_db_connection()
    if not conn:
        flash('Error de conexión a la base de datos', 'danger')
        return redirect(url_for('prods.listar'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, categoria_id, precio, stock) VALUES (%s, %s, %s, %s)",
                (nombre, categoria_id, precio, stock)
            )
            conn.commit()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('prods.listar'))
        except Exception as e:
            conn.rollback()
            flash(f'Error al crear producto: {str(e)}', 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    # Obtener categorías para el formulario
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        return render_template('prods/crear.html', categorias=categorias)
    except Exception as e:
        flash(f'Error al obtener categorías: {str(e)}', 'danger')
        return redirect(url_for('prods.listar'))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@prods_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db_connection()
    if not conn:
        flash('Error de conexión a la base de datos', 'danger')
        return redirect(url_for('prods.listar'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria_id = request.form['categoria_id']
        precio = request.form['precio']
        stock = request.form['stock']
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=%s, categoria_id=%s, precio=%s, stock=%s WHERE id=%s",
                (nombre, categoria_id, precio, stock, id)
            )
            conn.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('prods.listar'))
        except Exception as e:
            conn.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    # Obtener producto y categorías
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        prod = cursor.fetchone()
        
        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()
        
        if not prod:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('prods.listar'))
            
        return render_template('prods/editar.html', prod=prod, categorias=categorias)
    except Exception as e:
        flash(f'Error al obtener datos: {str(e)}', 'danger')
        return redirect(url_for('prods.listar'))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@prods_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'message': 'Error de conexión'})
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        flash('Producto eliminado exitosamente', 'success')
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 