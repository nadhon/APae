from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from flask import send_from_directory
from entities.paciente import Paciente
from extensions import db

bp = Blueprint('paciente_routes', __name__, url_prefix='/paciente')

@bp.route('/')
def index():
    pacientes = Paciente.query.all()
    return render_template('paciente/crud.html', pacientes=pacientes)

@bp.route('/create', methods=['POST'])
def create():
    try:
        novo = Paciente(
            nome=request.form['nome'],
            idade=int(request.form['idade']),
            email=request.form['email']
        )
        db.session.add(novo)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Erro ao criar paciente.')
    return redirect(url_for('paciente_routes.index'))

def allowed_file(filename):
    raise NotImplementedError

def secure_filename(filename):
    raise NotImplementedError

@bp.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado.')
            return redirect(url_for('paciente_routes.index'))
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(url_for('paciente_routes.index'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        flash('Nenhum arquivo enviado.')
    return redirect(url_for('paciente_routes.index'))
uploaded_files = [] 
@bp.route('/download/<filename>')
def download(filename):
    upload_folder = os.path.join('template', 'paciente', 'uploads')
    return send_from_directory(upload_folder, filename, as_attachment=True)

@bp.route('/delete/<int:id>')
def delete(id):
    p = Paciente.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('paciente_routes.index'))
