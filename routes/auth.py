from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from entities.admin import Admin
from extensions import db, login_manager

#import bcrypt

#senhaoriginal = b"senhateste"
#hashsenha = bcrypt.hashpq(senhaoriginal, bcrypt.gensalt())

#esperando banco de dados para começar os testes com hash...

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Admin.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Usuário ou senha inválidos.')
    return render_template('login.html', show_footer_and_nav=False)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
