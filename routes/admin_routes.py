from flask import Blueprint, render_template, request, redirect, url_for, flash
from entities.admin import Admin
from extensions import db

bp = Blueprint('admin_routes', __name__, url_prefix='/admin')

@bp.route('/')
def listar():
    admins = Admin.query.filter_by(ativo=True).all()
    return render_template('admin/listagem.html', admins=admins, show_footer_and_nav=False)

@bp.route('/inativos')
def listarInativos():
    admins = Admin.query.filter_by(ativo=False).all()
    return render_template('admin/listagem.html', admins=admins, show_footer_and_nav=False)

@bp.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'GET':
        return render_template('admin/crud.html', show_footer_and_nav=False)
    if request.method == 'POST':
        try:
            new_admin = Admin(username=request.form['username'], password=request.form['password'], email=request.form['email'], cargo=request.form['cargo'])
            db.session.add(new_admin)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('Erro ao criar colaborador.')
    return redirect(url_for('admin_routes.listar'))

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    admin = Admin.query.get_or_404(id)

    if request.method == 'GET':
        return render_template(
            'admin/editar.html',
            admin=admin,
            show_footer_and_nav=False
        )

    # POST: tenta salvar as alterações
    admin.username = request.form.get('username')
    admin.email = request.form.get('email')
    admin.cargo = request.form.get('cargo')

    # Se quiser permitir troca de senha somente quando preenchida:
    new_password = request.form.get('password')
    if new_password:
        admin.password = new_password  # supondo que o setter já faça hash

    try:
        db.session.commit()
        flash('Colaborador atualizado com sucesso!', 'success')
    except Exception:
        db.session.rollback()
        flash('Erro ao atualizar colaborador.', 'danger')

    return redirect(url_for('admin_routes.listar'))


@bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    admin = Admin.query.get_or_404(id)
    admin.ativo = False
    db.session.commit()
    flash("Colaborador marcado como inativo.", "info")
    return redirect(url_for('admin_routes.listar'))
