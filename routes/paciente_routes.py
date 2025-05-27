import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
from entities.paciente import Paciente
from extensions import db

bp = Blueprint('paciente_routes', __name__, url_prefix='/paciente')
UPLOAD_FODER = 'templates\paciente\uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

@bp.route('/upload', methods=['GET','POST'])
def allowed_file(filename):
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    return False
@bp.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = os.path.join('template', 'paciente', 'uploads')
            file.save(os.path.join(upload_folder, filename))
            flash('Arquivo enviado com sucesso!')
            return redirect(url_for('paciente_routes.index'))
    return render_template('paciente/crud.html') 
@bp.route('/download/<filename>')
def download_file(name):
    return send_from_directory(bp.config["UPLOAD_FOLDER"], name)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    p = Paciente.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('paciente_routes.index'))
