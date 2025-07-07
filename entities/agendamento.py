# entities/agendamento.py
from extensions import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = 'agendamento'

    id = db.Column(db.Integer, primary_key=True)
    nome_paciente = db.Column(db.String(150), nullable=False)
    cpf_paciente = db.Column(db.String(14), nullable=False)
    telefone_paciente = db.Column(db.String(20), nullable=True)
    data = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
