from flask import Blueprint, render_template, request, redirect, url_for, current_app
from app.db.models import get_db

products_bp = Blueprint("products", __name__)

@products_bp.route("/", methods=["GET", "POST"])
def index():
    db = get_db(current_app)

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        db.execute(
            "INSERT INTO products (nombre, cantidad, precio) VALUES (?, ?, ?)",
            (nombre, cantidad, precio)
        )
        db.commit()
        return redirect(url_for("products.index"))

    productos = db.execute("SELECT * FROM products").fetchall()
    return render_template("inventario/inventario.html", productos=productos)



@products_bp.route("/editar/<int:id>", methods=["POST"])
def editar(id):
    db = get_db(current_app)
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    db.execute(
        "UPDATE products SET nombre=?, cantidad=?, precio=? WHERE id=?",
        (nombre, cantidad, precio, id)
    )
    db.commit()
    return redirect(url_for("products.index"))


@products_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    db = get_db(current_app)
    db.execute("DELETE FROM products WHERE id=?", (id,))
    db.commit()
    return redirect(url_for("products.index"))
