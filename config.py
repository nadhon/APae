import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha_chave_secreta'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
