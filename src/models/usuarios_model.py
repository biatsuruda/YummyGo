from config_db import db 
from werkzeug.security import generate_password_hash, check_password_hash 

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=True) 
    telefone = db.Column(db.String(20), unique=True, nullable=True)
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True) 

    endereco = db.relationship('Endereco', backref='usuario', uselist=False)

    def __init__(self, nome, email, senha=None, telefone=None, google_id=None, profile_picture=None):
        self.nome = nome
        self.email = email
        self.set_senha(senha)
        self.telefone = telefone
        self.google_id = google_id
        self.profile_picture = profile_picture

    def set_senha(self, senha_texto):
        if senha_texto:
            self.senha = generate_password_hash(senha_texto, method='pbkdf2:sha256')
        else:
            self.senha = None

    def check_senha(self, senha_texto):
        return self.senha and check_password_hash(self.senha, senha_texto)

    def __repr__(self):
        return f'<Usuario {self.nome} ({self.email})>'