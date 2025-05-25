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
@bp.route('/upload', methods=['POST'])
def upload():
    arquivo = request.files.get('arquivo')
    if arquivo and arquivo.filename.lower().endswith('.pdf'):
        upload_folder = os.path.join('template', 'paciente', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        pdf_filename = arquivo.filename
        caminho = os.path.join(upload_folder, arquivo.filename)
        arquivo.save(caminho)
        flash('Arquivo enviado com sucesso.')
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
