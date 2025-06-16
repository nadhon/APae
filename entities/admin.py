from extensions import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

