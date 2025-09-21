from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.db.models import get_db
import os, json

products_bp = Blueprint("products", __name__)

        # GESTION DE PRODUCTOS 
@products_bp.route("/", methods=["GET", "POST"])
def index():
    db = get_db(current_app)

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        # Guardar sqlite
        cursor = db.execute(
            "INSERT INTO products (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre, cantidad, precio)
        )
        db.commit()
        producto_id = cursor.lastrowid  # ID autoincremental

        # Guardar en json 
        datos_dir = os.path.join(current_app.root_path, "..", "datos")
        os.makedirs(datos_dir, exist_ok=True)
        json_path = os.path.join(datos_dir, "datos.json")

        productos_json = []
        if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    productos_json = json.load(f)
                except json.JSONDecodeError:
                    productos_json = []

        productos_json.append({
            "id": producto_id,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio": precio
        })

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(productos_json, f, indent=4, ensure_ascii=False)

        return redirect(url_for("products.index"))

    # Mostrar productos
    productos = db.execute("SELECT * FROM products").fetchall()
    return render_template("inventario/inventario.html", productos=productos)

# EDITAR 
@products_bp.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    db = get_db(current_app)
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    # actualizar en sqlite
    db.execute(
        "UPDATE products SET nombre=?, cantidad=?, precio=? WHERE id=?",
        (nombre, cantidad, precio, id)
    )
    db.commit()

    #  Actualizar el json
    datos_dir = os.path.join(current_app.root_path, "..", "datos")
    json_path = os.path.join(datos_dir, "datos.json")

    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, "r", encoding="utf-8") as f:
            productos_json = json.load(f)

        for p in productos_json:
            if p.get("id") == id:
                p["nombre"] = nombre
                p["cantidad"] = cantidad
                p["precio"] = precio

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(productos_json, f, indent=4, ensure_ascii=False)

    return redirect(url_for("products.index"))

# ELIMINAR
@products_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    db = get_db(current_app)
    db.execute("DELETE FROM products WHERE id=?", (id,))
    db.commit()

    #Eliminar del JSON
    datos_dir = os.path.join(current_app.root_path, "..", "datos")
    json_path = os.path.join(datos_dir, "datos.json")

    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, "r", encoding="utf-8") as f:
            productos_json = json.load(f)

        productos_json = [p for p in productos_json if p.get("id") != id]

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(productos_json, f, indent=4, ensure_ascii=False)

    return redirect(url_for("products.index"))
