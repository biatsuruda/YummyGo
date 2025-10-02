from config_db import db

class Restaurante(db.Model):
    __tablename__ = 'restaurante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(15))
    categoria = db.Column(db.String(50))
    endereco_id = db.Column(db.Integer, db.ForeignKey('endereco.id'), nullable=True)

    endereco = db.relationship('Endereco', backref='restaurante', uselist=False)

    def __init__(self, nome, cnpj, telefone, categoria, endereco=None):
        self.nome = nome
        self.cnpj = cnpj
        self.telefone = telefone
        self.categoria = categoria
        self.endereco = endereco

    def __repr__(self):
        return f'<Restaurante {self.nome}>'
    
from src.models.endereco_model import Endereco
Restaurante.endereco = db.relationship("Endereco", backref="restaurante", uselist=False)