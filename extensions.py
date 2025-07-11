from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# instâncias únicas para toda a app
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
