from extensions import db
from entities.mae import Mae
from entities.pai import Pai
from entities.responsavel import Responsavel
from entities.saude import Saude
from entities.agendamento import Agendamento
from sqlalchemy.orm import relationship
from sqlalchemy import JSON

class Paciente(db.Model):
    __tablename__ = 'paciente'

    ativo = db.Column(db.Boolean, default=True)

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    nome_social = db.Column(db.String(150))
    prontuario = db.Column(db.String(50))
    situacao_cadastro = db.Column(db.String(50))
    area_atendimento = db.Column(db.String(50))
    data_entrada = db.Column(db.Date)
    data_saida = db.Column(db.Date)
    cpf = db.Column(db.String(14))
    rg = db.Column(db.String(20))
    data_emissao_rg = db.Column(db.Date)
    certidao_nascimento = db.Column(db.String(50))
    livro = db.Column(db.String(20))
    folha = db.Column(db.String(20))
    cartorio = db.Column(db.String(100))
    naturalidade = db.Column(db.String(100))
    sexo = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    ocupacao = db.Column(db.String(100))
    carteira_pcd = db.Column(db.String(50))
    cartao_nis = db.Column(db.String(50))
    cartao_sus = db.Column(db.String(50))
    raca_cor = db.Column(db.String(30))
    mobilidade = db.Column(JSON, nullable=True)
    tipo_deficiencia = db.Column(JSON, nullable=True)
    transtornos = db.Column(JSON, nullable=True)
    cid10_1 = db.Column(db.String(20))
    cid10_2 = db.Column(db.String(20))
    cid10_3 = db.Column(db.String(20))
    cid10_4 = db.Column(db.String(20))
    cid11 = db.Column(db.String(20))
    cep = db.Column(db.String(10))
    endereco = db.Column(db.String(150))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    email = db.Column(db.String(100))
    telefone_residencial = db.Column(db.String(20))
    telefone_recados = db.Column(db.String(20))
    pessoa_contato = db.Column(db.String(100))

    mae_id = db.Column(db.Integer, db.ForeignKey('mae.id'))
    pai_id = db.Column(db.Integer, db.ForeignKey('pai.id'))
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'))
    saude_id = db.Column(db.Integer, db.ForeignKey('saude.id'))

    mae = relationship('Mae', backref='pacientes')
    pai = relationship('Pai', backref='pacientes')
    responsavel = relationship('Responsavel', backref='pacientes')
    saude = relationship('Saude', backref='pacientes')
    
