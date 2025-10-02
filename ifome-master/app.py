from flask import Flask
from config_db import db
import os
from dotenv import load_dotenv
def create_app():
    app = Flask(__name__, static_folder='src/static')
    
    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifome.db'  # Exemplo com SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Inicializa o SQLAlchemy com o app
    db.init_app(app)

    from src.controllers.usuarios import usuarios_bp
    from src.controllers.home import home_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)

    return app

# Este bloco só será executado quando você rodar o script diretamente
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
    