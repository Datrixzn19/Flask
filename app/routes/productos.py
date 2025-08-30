from flask import Blueprint, render_template 



productos = Blueprint("productos",__name__ , url_prefix=('/productos'))

@productos.route('/products')
def products():
    return render_template('inventario/inventario.html')


@productos.route('/nuevo')
def agregar():
    return render_template('inventario/nuevoProducto.html')

