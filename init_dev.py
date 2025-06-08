import os
from app import create_app
from extensions import db
from entities.admin import Admin

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app = create_app()

with app.app_context():
    if not os.path.exists(DB_PATH):
        db.create_all()
        print("Banco de dados SQLite criado com sucesso.")
    else:
        print("Banco de dados já existe.")

    # Verifica se já existe um admin de teste
    username = 'admin'
    password = 'admin'

    if Admin.query.filter_by(username=username).first():
        print(f"Usuário admin '{username}' já existe.")
    else:
        admin = Admin(username=username, password=password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin de teste criado: {username} / {password}")
