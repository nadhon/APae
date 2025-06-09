from extensions import db

class Saude(db.Model):
    __tablename__ = 'saude'

    id = db.Column(db.Integer, primary_key=True)
    utiliza_medicamentos = db.Column(db.String(20))
    quais_medicamentos = db.Column(db.Text)
    possui_alergia = db.Column(db.String(20))
    quais_alergias = db.Column(db.Text)
    possui_comorbidade = db.Column(db.String(20))
    quais_comorbidades = db.Column(db.Text)
    possui_convenio = db.Column(db.String(20))
    qual_convenio = db.Column(db.Text)
    liberado_atividade_fisica = db.Column(db.String(20))
    data_liberacao = db.Column(db.Date)
    transporte_ida = db.Column(db.String(100))
    transporte_volta = db.Column(db.String(100))
    autorizacao_imagem = db.Column(db.String(20))
    observacoes = db.Column(db.Text)
