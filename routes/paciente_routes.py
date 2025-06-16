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
    query = Paciente.query.filter_by(ativo=True)

    if filtro_nome:
        query = query.filter(Paciente.nome.ilike(f"%{filtro_nome}%"))
    if filtro_cpf:
        query = query.filter(Paciente.cpf.ilike(f"%{filtro_cpf}%"))

    pacientes = query.all()
    return render_template('paciente/listagem.html', pacientes=pacientes, show_footer_and_nav=False)

# Remover isto em produção
@bp.route('/inativos')
def listar_inativos():
    pacientes = Paciente.query.filter_by(ativo=False).all()
    return render_template('paciente/listagem.html', pacientes=pacientes, show_footer_and_nav=False)

@bp.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'GET':
        return render_template('paciente/crud.html', show_footer_and_nav=False)

    # POST
    data_liberacao = parse_date(request.form.get('data_liberacao'))

    # Criando registros relacionados
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
        utiliza_medicamentos=request.form.get('usa_medicamentos'),
        quais_medicamentos=request.form.get('qual_medicamentos'),
        possui_alergia=request.form.get('possui_alergia'),
        quais_alergias=request.form.get('qual_alergias'),
        possui_comorbidade=request.form.get('possui_comorbidade'),
        quais_comorbidades=request.form.get('qual_comorbidades'),
        possui_convenio=request.form.get('convenio_medico'),
        qual_convenio=request.form.get('qual_convenio'),
        liberado_atividade_fisica=request.form.get('liberado_atividade'),
        data_liberacao=data_liberacao,
        transporte_ida=request.form.get('meio_transporte_ida'),
        transporte_volta=request.form.get('meio_transporte_volta'),
        autorizacao_imagem=request.form.get('autorizacao_imagem'),
        observacoes=request.form.get('observacoes_saude')
    )

    db.session.add_all([mae, pai, responsavel, saude])
    db.session.flush()

    # Criando paciente
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
        certidao_nascimento=request.form.get('certidao'),
        livro=request.form.get('livro'),
        folha=request.form.get('folha'),
        cartorio=request.form.get('cartorio'),
        naturalidade=request.form.get('naturalidade'),
        sexo=request.form.get('sexo'),
        data_nascimento=parse_date(request.form.get('data_nascimento')),
        ocupacao=request.form.get('ocupacao'),
        carteira_pcd=request.form.get('carteira_pcd'),
        cartao_nis=request.form.get('nis'),
        cartao_sus=request.form.get('sus'),
        raca_cor=request.form.get('raca_cor'),
        mobilidade=request.form.getlist('mobilidade'),
        tipo_deficiencia=request.form.getlist('tipo_deficiencia'),
        transtornos=request.form.getlist('transtornos'),
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
        pessoa_contato=request.form.get('contato'),
        mae_id=mae.id,
        pai_id=pai.id,
        responsavel_id=responsavel.id,
        saude_id=saude.id
    )

    db.session.add(paciente)
    db.session.commit()
    flash("Paciente cadastrado com sucesso!", "success")
    return redirect(url_for('paciente_routes.listar'))

@bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    paciente = Paciente.query.get_or_404(id)
    mae = paciente.mae
    pai = paciente.pai
    responsavel = paciente.responsavel
    saude = paciente.saude

    if request.method == 'GET':
        return render_template(
            'paciente/editar.html',
            paciente=paciente,
            mae=mae,
            pai=pai,
            responsavel=responsavel,
            saude=saude,
            show_footer_and_nav=False
        )

    # POST
    data_liberacao = parse_date(request.form.get('data_liberacao'))

    # Dados da mãe
    mae.nome = request.form.get('mae_nome')
    mae.cpf = request.form.get('mae_cpf')
    mae.telefone = request.form.get('mae_telefone')
    mae.email = request.form.get('mae_email')
    mae.ocupacao = request.form.get('mae_ocupacao')

    # Dados do pai
    pai.nome = request.form.get('pai_nome')
    pai.cpf = request.form.get('pai_cpf')
    pai.telefone = request.form.get('pai_telefone')
    pai.email = request.form.get('pai_email')
    pai.ocupacao = request.form.get('pai_ocupacao')

    # Dados do responsável
    responsavel.nome = request.form.get('resp_nome')
    responsavel.cpf = request.form.get('resp_cpf')
    responsavel.telefone = request.form.get('resp_telefone')
    responsavel.email = request.form.get('resp_email')
    responsavel.ocupacao = request.form.get('resp_ocupacao')

    # Dados de saúde
    saude.utiliza_medicamentos = request.form.get('usa_medicamentos')
    saude.quais_medicamentos = request.form.get('qual_medicamentos')
    saude.possui_alergia = request.form.get('possui_alergia')
    saude.quais_alergias = request.form.get('qual_alergias')
    saude.possui_comorbidade = request.form.get('possui_comorbidade')
    saude.quais_comorbidades = request.form.get('qual_comorbidades')
    saude.possui_convenio = request.form.get('convenio_medico')
    saude.qual_convenio = request.form.get('qual_convenio')
    saude.liberado_atividade_fisica = request.form.get('liberado_atividade')
    saude.data_liberacao = data_liberacao
    saude.transporte_ida = request.form.get('meio_transporte_ida')
    saude.transporte_volta = request.form.get('meio_transporte_volta')
    saude.autorizacao_imagem = request.form.get('autorizacao_imagem')
    saude.observacoes = request.form.get('observacoes_saude')

    # Dados do paciente
    paciente.nome = request.form.get('nome')
    paciente.nome_social = request.form.get('nome_social')
    paciente.prontuario = request.form.get('prontuario')
    paciente.situacao_cadastro = request.form.get('situacao_cadastro')
    paciente.area_atendimento = request.form.get('area_atendimento')
    paciente.data_entrada = parse_date(request.form.get('data_entrada'))
    paciente.data_saida = parse_date(request.form.get('data_saida'))
    paciente.cpf = request.form.get('cpf')
    paciente.rg = request.form.get('rg')
    paciente.data_emissao_rg = parse_date(request.form.get('data_emissao_rg'))
    paciente.certidao_nascimento = request.form.get('certidao')
    paciente.livro = request.form.get('livro')
    paciente.folha = request.form.get('folha')
    paciente.cartorio = request.form.get('cartorio')
    paciente.naturalidade = request.form.get('naturalidade')
    paciente.sexo = request.form.get('sexo')
    paciente.data_nascimento = parse_date(request.form.get('data_nascimento'))
    paciente.ocupacao = request.form.get('ocupacao')
    paciente.carteira_pcd = request.form.get('carteira_pcd')
    paciente.cartao_nis = request.form.get('nis')
    paciente.cartao_sus = request.form.get('sus')
    paciente.raca_cor = request.form.get('raca_cor')
    paciente.mobilidade = request.form.getlist('mobilidade')
    paciente.tipo_deficiencia = request.form.getlist('tipo_deficiencia')
    paciente.transtornos = request.form.getlist('transtornos')
    paciente.cid10_1 = request.form.get('cid10_1')
    paciente.cid10_2 = request.form.get('cid10_2')
    paciente.cid10_3 = request.form.get('cid10_3')
    paciente.cid10_4 = request.form.get('cid10_4')
    paciente.cid11 = request.form.get('cid11')
    paciente.cep = request.form.get('cep')
    paciente.endereco = request.form.get('endereco')
    paciente.numero = request.form.get('numero')
    paciente.complemento = request.form.get('complemento')
    paciente.bairro = request.form.get('bairro')
    paciente.cidade = request.form.get('cidade')
    paciente.uf = request.form.get('uf')
    paciente.email = request.form.get('email')
    paciente.telefone_residencial = request.form.get('telefone_residencial')
    paciente.telefone_recados = request.form.get('telefone_recados')
    paciente.pessoa_contato = request.form.get('contato')

    db.session.commit()
    flash("Paciente atualizado com sucesso!", "success")
    return redirect(url_for('paciente_routes.listar'))

@bp.route('/<int:id>/deletar', methods=['POST'])
def deletar(id):
    paciente = Paciente.query.get_or_404(id)
    paciente.ativo = False
    db.session.commit()
    flash("Paciente marcado como inativo.", "info")
    return redirect(url_for('paciente_routes.listar'))
