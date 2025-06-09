from extensions import db

class Pai(db.Model):
    __tablename__ = 'pai'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(14))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    ocupacao = db.Column(db.String(100))
