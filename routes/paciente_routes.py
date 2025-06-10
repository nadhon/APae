from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory
from extensions import db
from entities.paciente import Paciente
from entities.mae import Mae
from entities.pai import Pai
from entities.responsavel import Responsavel
from entities.saude import Saude
from datetime import datetime

bp = Blueprint('paciente_routes', __name__, template_folder='templates/paciente', url_prefix='/paciente')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'docx', 'doc', 'txt'}

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

@bp.route('/')
def listar():
    filtro_nome = request.args.get('nome')
    filtro_cpf = request.args.get('cpf')
    query = Paciente.query

    if filtro_nome:
        query = query.filter(Paciente.nome.ilike(f"%{filtro_nome}%"))
    if filtro_cpf:
        query = query.filter(Paciente.cpf.ilike(f"%{filtro_cpf}%"))

    pacientes = query.all()
    return render_template('paciente/listagem.html', pacientes=pacientes, show_footer_and_nav=False)

@bp.route('/novo', methods=['GET', 'POST'])
def novo():

    if request.method == 'GET':
        return render_template('paciente/crud.html', show_footer_and_nav=False)

    if request.method == 'POST':
        data_liberacao = parse_date(request.form.get('data_liberacao'))

        mae = Mae(
            nome=request.form.get('mae_nome'),
            cpf=request.form.get('mae_cpf'),
            telefone=request.form.get('mae_telefone'),
            email=request.form.get('mae_email'),
            ocupacao=request.form.get('mae_ocupacao')
        )
        pai = Pai(
            nome=request.form.get('pai_nome'),
            cpf=request.form.get('pai_cpf'),
            telefone=request.form.get('pai_telefone'),
            email=request.form.get('pai_email'),
            ocupacao=request.form.get('pai_ocupacao')
        )
        responsavel = Responsavel(
            nome=request.form.get('resp_nome'),
            cpf=request.form.get('resp_cpf'),
            telefone=request.form.get('resp_telefone'),
            email=request.form.get('resp_email'),
            ocupacao=request.form.get('resp_ocupacao')
        )
        saude = Saude(
            utiliza_medicamentos=request.form.get('usa_medicamento'),
            quais_medicamentos=request.form.get('quais_medicamentos'),
            possui_alergia=request.form.get('possui_alergia'),
            quais_alergias=request.form.get('quais_alergias'),
            possui_comorbidade=request.form.get('possui_comorbidade'),
            quais_comorbidades=request.form.get('quais_comorbidades'),
            possui_convenio=request.form.get('possui_convenio'),
            qual_convenio=request.form.get('qual_convenio'),
            liberado_atividade_fisica=request.form.get('liberado_af'),
            data_liberacao=data_liberacao,
            transporte_ida=request.form.get('transporte_ida'),
            transporte_volta=request.form.get('transporte_volta'),
            autorizacao_imagem=request.form.get('autorizacao_imagem'),
            observacoes=request.form.get('observacoes')
        )

        db.session.add_all([mae, pai, responsavel, saude])
        db.session.flush()

        paciente = Paciente(
            nome=request.form.get('nome'),
            nome_social=request.form.get('nome_social'),
            prontuario=request.form.get('prontuario'),
            situacao_cadastro=request.form.get('situacao_cadastro'),
            area_atendimento=request.form.get('area_atendimento'),
            data_entrada=parse_date(request.form.get('data_entrada')),
            data_saida=parse_date(request.form.get('data_saida')),
            cpf=request.form.get('cpf'),
            rg=request.form.get('rg'),
            data_emissao_rg=parse_date(request.form.get('data_emissao_rg')),
            certidao_nascimento=request.form.get('certidao_nascimento'),
            livro=request.form.get('livro'),
            folha=request.form.get('folha'),
            cartorio=request.form.get('cartorio'),
            naturalidade=request.form.get('naturalidade'),
            sexo=request.form.get('sexo'),
            data_nascimento=parse_date(request.form.get('data_nascimento')),
            ocupacao=request.form.get('ocupacao'),
            carteira_pcd=request.form.get('carteira_pcd'),
            cartao_nis=request.form.get('cartao_nis'),
            cartao_sus=request.form.get('cartao_sus'),
            raca_cor=request.form.get('raca_cor'),
            mobilidade=request.form.get('mobilidade'),
            tipo_deficiencia=request.form.get('tipo_deficiencia'),
            transtornos=request.form.get('transtornos'),
            cid10_1=request.form.get('cid10_1'),
            cid10_2=request.form.get('cid10_2'),
            cid10_3=request.form.get('cid10_3'),
            cid10_4=request.form.get('cid10_4'),
            cid11=request.form.get('cid11'),
            cep=request.form.get('cep'),
            endereco=request.form.get('endereco'),
            numero=request.form.get('numero'),
            complemento=request.form.get('complemento'),
            bairro=request.form.get('bairro'),
            cidade=request.form.get('cidade'),
            uf=request.form.get('uf'),
            email=request.form.get('email'),
            telefone_residencial=request.form.get('telefone_residencial'),
            telefone_recados=request.form.get('telefone_recados'),
            pessoa_contato=request.form.get('pessoa_contato'),
            mae_id=mae.id,
            pai_id=pai.id,
            responsavel_id=responsavel.id,
            saude_id=saude.id
        )

        db.session.add(paciente)
        db.session.commit()
        flash("Paciente cadastrado com sucesso!", "success")
        return redirect(url_for('paciente_routes.listar'))

    return redirect(url_for('paciente_routes.listar'))

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    paciente = Paciente.query.get_or_404(id)
    if request.method == 'POST':
        paciente.nome = request.form.get('nome')
        paciente.cpf = request.form.get('cpf')
        paciente.rg = request.form.get('rg')
        db.session.commit()
        flash("Paciente atualizado com sucesso!", "success")
        return redirect(url_for('paciente_routes.listar'))

    return redirect(url_for('paciente_routes.listar'))

@bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash("Paciente removido com sucesso.", "info")
    return redirect(url_for('paciente_routes.listar'))
