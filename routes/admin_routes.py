from flask import Blueprint, render_template, request, redirect, url_for, flash
from entities.admin import Admin
from extensions import db

bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@bp.route('/')
def listar():
    admins = Admin.query.all()
    return render_template('admin/listagem.html', admins=admins, show_footer_and_nav=False)

@bp.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'GET':
        return render_template('admin/crud.html', show_footer_and_nav=False)
    if request.method == 'POST':
        try:
            new_admin = Admin(username=request.form['username'], password=request.form['password'])
            db.session.add(new_admin)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Erro ao criar admin.')
    return redirect(url_for('admin_routes.listar'))

@bp.route('/delete/<int:id>')
def delete(id):
    a = Admin.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('admin_routes.index'))
