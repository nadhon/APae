from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory
import os
from entities.paciente import Paciente
from extensions import db

bp = Blueprint('paciente_routes', __name__, url_prefix='/paciente' )
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'doc', 'txt'}


@bp.route('/')
def index():
    pacientes = Paciente.query.all()
    return render_template('paciente/crud.html', pacientes=pacientes, show_footer_and_nav=False)

@bp.route('/create', methods=['POST'])
def create():
    nome = request.form['nome']
    idade = int(request.form['idade'])
    email = request.form['email']
    arquivo = request.files.get('arquivo')
    filename= None
    if arquivo and allowed_file(arquivo.filename): 
        filename = secure_filename(arquivo.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        arquivo.save(os.path.join(upload_folder, filename))
    novo = Paciente(nome=nome, idade=idade, email=email, arquivo=filename)
    db.session.add(novo)
    db.session.commit()
    flash('Paciente adicionado com sucesso!')
    return redirect(url_for('paciente_routes.index'))
@bp.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True) # type: ignore
    except FileNotFoundError:
        flash('Arquivo não encontrado.', 'error')
        return redirect(url_for('paciente_routes.index'))
    
@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    p = Paciente.query.get_or_404(id)
    if p.arquivo:
        arquivo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], p.arquivo)
        if os.path.exists(arquivo_path):
            os.remove(arquivo_path)
    db.session.delete(p)
    db.session.commit()
    flash('Paciente removido com sucesso!')
    return redirect(url_for('paciente_routes.index'))