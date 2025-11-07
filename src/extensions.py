"""
Este ficheiro centraliza a declaração de todas as extensões do Flask.

Ao declarar as instâncias aqui (ex: db = SQLAlchemy()), evitamos 
importações circulares.

A inicialização real (ex: db.init_app(app)) acontece dentro da factory
create_app() em src/__init__.py.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

# Base de Dados
db = SQLAlchemy()
migrate = Migrate()

# Segurança e Autenticação
bcrypt = Bcrypt()
login_manager = LoginManager()
oauth = OAuth()
mail = Mail()

# --- Configuração do LoginManager ---
# Para onde o Flask-Login deve redirecionar o utilizador se ele tentar
# aceder a uma página protegida sem estar logado.
login_manager.login_view = 'auth.login' 

# Mensagem exibida ao ser redirecionado (opcional, mas útil)
login_manager.login_message = 'Por favor, faça login para aceder a esta página.'
login_manager.login_message_category = 'info' # Categoria para flashes (mensagens)