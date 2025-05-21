from flask import Flask
from config import Config
from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)

    # registra o loader após login_manager estar pronto
    from entities.admin import Admin
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # importa entidades e rotas
    from entities import paciente  # admin já carregado acima
    from routes import auth, dashboard, admin_routes, paciente_routes, errors

    # registra blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(paciente_routes.bp)
    app.register_blueprint(errors.errors)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
