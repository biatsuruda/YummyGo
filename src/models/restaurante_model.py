from config_db import db
from datetime import datetime 

class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False) 
    cnpj = db.Column(db.String(18), unique=True, nullable=False) 
    telefone = db.Column(db.String(20), nullable=True) 
    email = db.Column(db.String(120), unique=True, nullable=True) 
    
    descricao = db.Column(db.Text, nullable=True) 
    categoria = db.Column(db.String(50), nullable=True) 
    
    # Informações de entrega e avaliação
    tempo_medio_entrega_min = db.Column(db.Integer, default=30) # Tempo mínimo em minutos
    tempo_medio_entrega_max = db.Column(db.Integer, default=60) # Tempo máximo em minutos
    taxa_entrega = db.Column(db.Numeric(10, 2), default=0.00) # Custo da taxa de entrega
    avaliacao_media = db.Column(db.Numeric(2, 1), default=0.0) # Avaliação de 0.0 a 5.0

    # URLs para logo e capa
    url_logo = db.Column(db.String(255), nullable=True)
    url_capa = db.Column(db.String(255), nullable=True)
    
    is_active = db.Column(db.Boolean, default=True) # Se o restaurante está ativo na plataforma
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow) # Data de cadastro

    # Chave estrangeira para Endereco
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)
    endereco = db.relationship('Endereco', backref='restaurante', uselist=False)

    def __init__(self, nome, cnpj, telefone=None, email=None, descricao=None, categoria=None,
                 tempo_medio_entrega_min=30, tempo_medio_entrega_max=60, taxa_entrega=0.00,
                 url_logo=None, url_capa=None, is_active=True, endereco=None):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.email = email
        self.descricao = descricao
        self.categoria = categoria
        self.tempo_medio_entrega_min = tempo_medio_entrega_min
        self.tempo_medio_entrega_max = tempo_medio_entrega_max
        self.taxa_entrega = taxa_entrega
        self.url_logo = url_logo
        self.url_capa = url_capa
        self.is_active = is_active
        if endereco:
            self.endereco = endereco

    def __repr__(self):
        return f'<Restaurante {self.nome}>'