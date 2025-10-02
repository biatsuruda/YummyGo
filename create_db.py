from app import create_app
from config_db import db

# Importa todos os models para o SQLAlchemy "conhecer"
from src.models.usuarios_model import Usuarios
from src.models.endereco_model import Endereco
from src.models.restaurante_model import Restaurante
app = create_app()

with app.app_context():
    db.create_all()
    print("Banco e tabelas criados com sucesso!")