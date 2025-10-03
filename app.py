from flask import Flask, session
from config_db import db
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_moment import Moment


def create_app():
    load_dotenv()

    app = Flask(__name__, static_folder='src/static', template_folder='templates') 
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifome.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta_padrao_muito_segura') 
    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID') 
    
    if not app.config['GOOGLE_CLIENT_ID']:
        print("AVISO: Variável de ambiente GOOGLE_CLIENT_ID não definida no app.config!")

    db.init_app(app)
    Moment(app)
    
    # Importe os blueprints aqui
    from src.controllers.usuarios import usuarios_bp
    from src.controllers.home import home_bp
    from src.controllers.carrinho import carrinho_bp
    from src.controllers.institucional import institucional_bp

    # Registre os blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(institucional_bp)
    
    @app.context_processor
    def inject_global_vars():
        return dict(current_year=datetime.now().year,
                    GOOGLE_CLIENT_ID=app.config['GOOGLE_CLIENT_ID']) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)