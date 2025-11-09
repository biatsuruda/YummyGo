from src.extensions import db
import datetime

# -------------------------
# Modelo Restaurante
# -------------------------
class Restaurante(db.Model):
    __tablename__ = 'restaurantes'

    id = db.Column(db.Integer, primary_key=True)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    razao_social = db.Column(db.String(100), unique=True, nullable=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    logo_url = db.Column(db.String(255), nullable=True)
    tempo_medio_entrega = db.Column(db.Integer, nullable=True)
    taxa_entrega = db.Column(db.Float, nullable=True)
    ativo = db.Column(db.Boolean, default=False)

    # Relacionamentos
    categorias = db.relationship(
        'src.models.menu_model.Categoria',
        backref='restaurante',
        lazy=True,
        cascade="all, delete-orphan"
    )
    produtos = db.relationship(
        'src.models.menu_model.Produto',
        backref='restaurante',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Restaurante {self.nome_fantasia}>'

# -------------------------
# Modelo Endereco
# -------------------------
class Endereco(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Endereco {self.rua}, {self.numero} - {self.cidade}>'

# -------------------------
# Modelo Categoria
# -------------------------
class Categoria(db.Model):
    __tablename__ = 'categorias'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)

    produtos = db.relationship(
        'Produto',
        backref='categoria',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Categoria {self.nome}>'

# -------------------------
# Modelo Produto
# -------------------------
class Produto(db.Model):
    __tablename__ = 'produtos'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    disponivel = db.Column(db.Boolean, default=True)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)

    # RELAÇÃO COM ITENS DE PEDIDO
    itens_pedido = db.relationship(
        'ItemPedido',
        backref='produto',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Produto {self.nome} - R${self.preco:.2f}>'
