from extensions import db

class Mae(db.Model):
    __tablename__ = 'mae'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(14))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    ocupacao = db.Column(db.String(100))
