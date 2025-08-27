from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register')
def register():
    return render_template('auth/register.html')
