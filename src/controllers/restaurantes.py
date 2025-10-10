from flask import Blueprint, request, jsonify
from config_db import db
from src.models.restaurante_model import Restaurante
from src.models.endereco_model import Endereco # Para criar/atualizar endereços associados
from datetime import datetime

restaurantes_bp = Blueprint('restaurantes', __name__, url_prefix='/api/restaurantes')

# Helper para serializar um restaurante para JSON
def serialize_restaurante(restaurante):
    endereco_data = None
    if restaurante.endereco:
        endereco_data = {
            'id': restaurante.endereco.id,
            'rua': restaurante.endereco.rua,
            'numero': restaurante.endereco.numero,
            'complemento': restaurante.endereco.complemento,
            'bairro': restaurante.endereco.bairro,
            'cidade': restaurante.endereco.cidade,
            'estado': restaurante.endereco.estado,
            'cep': restaurante.endereco.cep
        }
    
    return {
        'id': restaurante.id,
        'nome': restaurante.nome,
        'cnpj': restaurante.cnpj,
        'telefone': restaurante.telefone,
        'email': restaurante.email,
        'descricao': restaurante.descricao,
        'categoria': restaurante.categoria,
        'tempo_medio_entrega_min': restaurante.tempo_medio_entrega_min,
        'tempo_medio_entrega_max': restaurante.tempo_medio_entrega_max,
        'taxa_entrega': float(restaurante.taxa_entrega), # Converter para float para JSON
        'avaliacao_media': float(restaurante.avaliacao_media), # Converter para float para JSON
        'url_logo': restaurante.url_logo,
        'url_capa': restaurante.url_capa,
        'is_active': restaurante.is_active,
        'data_cadastro': restaurante.data_cadastro.isoformat(),
        'endereco': endereco_data
    }

# ROTA PARA CRIAR NOVO RESTAURANTE (POST)
@restaurantes_bp.route('/', methods=['POST'])
def create_restaurante():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados JSON inválidos ou ausentes"}), 400

    # Validar campos obrigatórios
    required_fields = ['nome', 'cnpj', 'endereco_rua', 'endereco_numero', 'endereco_bairro', 'endereco_cidade', 'endereco_estado', 'endereco_cep']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"Campo obrigatório '{field}' ausente ou vazio"}), 400

    # Verificar unicidade (nome, cnpj, email)
    if Restaurante.query.filter_by(nome=data['nome']).first():
        return jsonify({"message": "Nome de restaurante já cadastrado"}), 409
    if Restaurante.query.filter_by(cnpj=data['cnpj']).first():
        return jsonify({"message": "CNPJ já cadastrado"}), 409
    if 'email' in data and data['email'] and Restaurante.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email de restaurante já cadastrado"}), 409

    try:
        # Criar Endereço primeiro
        novo_endereco = Endereco(
            rua=data['endereco_rua'],
            numero=data.get('endereco_numero'),
            complemento=data.get('endereco_complemento'),
            bairro=data['endereco_bairro'],
            cidade=data['endereco_cidade'],
            estado=data['endereco_estado'],
            cep=data['endereco_cep']
        )
        db.session.add(novo_endereco)
        db.session.flush() # Para ter o ID do endereço antes de criar o restaurante

        # Criar Restaurante
        novo_restaurante = Restaurante(
            nome=data['nome'],
            cnpj=data['cnpj'],
            telefone=data.get('telefone'),
            email=data.get('email'),
            descricao=data.get('descricao'),
            categoria=data.get('categoria'),
            tempo_medio_entrega_min=data.get('tempo_medio_entrega_min', 30),
            tempo_medio_entrega_max=data.get('tempo_medio_entrega_max', 60),
            taxa_entrega=data.get('taxa_entrega', 0.00),
            url_logo=data.get('url_logo'),
            url_capa=data.get('url_capa'),
            is_active=data.get('is_active', True),
            endereco=novo_endereco # Associar o endereço criado
        )
        db.session.add(novo_restaurante)
        db.session.commit()
        return jsonify(serialize_restaurante(novo_restaurante)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao criar restaurante", "error": str(e)}), 500

# ROTA PARA LISTAR TODOS OS RESTAURANTES (GET)
@restaurantes_bp.route('/', methods=['GET'])
def get_restaurantes():
    restaurantes = Restaurante.query.all()
    return jsonify([serialize_restaurante(r) for r in restaurantes]), 200

# ROTA PARA OBTER UM RESTAURANTE ESPECÍFICO POR ID (GET)
@restaurantes_bp.route('/<int:restaurante_id>', methods=['GET'])
def get_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if not restaurante:
        return jsonify({"message": "Restaurante não encontrado"}), 404
    return jsonify(serialize_restaurante(restaurante)), 200

# ROTA PARA ATUALIZAR UM RESTAURANTE EXISTENTE (PUT)
@restaurantes_bp.route('/<int:restaurante_id>', methods=['PUT'])
def update_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if not restaurante:
        return jsonify({"message": "Restaurante não encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados JSON inválidos ou ausentes"}), 400

    try:
        # Atualizar campos do Restaurante
        restaurante.nome = data.get('nome', restaurante.nome)
        restaurante.telefone = data.get('telefone', restaurante.telefone)
        restaurante.email = data.get('email', restaurante.email)
        restaurante.descricao = data.get('descricao', restaurante.descricao)
        restaurante.categoria = data.get('categoria', restaurante.categoria)
        restaurante.tempo_medio_entrega_min = data.get('tempo_medio_entrega_min', restaurante.tempo_medio_entrega_min)
        restaurante.tempo_medio_entrega_max = data.get('tempo_medio_entrega_max', restaurante.tempo_medio_entrega_max)
        restaurante.taxa_entrega = data.get('taxa_entrega', restaurante.taxa_entrega)
        restaurante.url_logo = data.get('url_logo', restaurante.url_logo)
        restaurante.url_capa = data.get('url_capa', restaurante.url_capa)
        restaurante.is_active = data.get('is_active', restaurante.is_active)

    
        if 'cnpj' in data and data['cnpj'] != restaurante.cnpj:
            if Restaurante.query.filter_by(cnpj=data['cnpj']).first():
                return jsonify({"message": "CNPJ já cadastrado para outro restaurante"}), 409
            restaurante.cnpj = data['cnpj']
        
        if 'email' in data and data['email'] and data['email'] != restaurante.email:
            if Restaurante.query.filter_by(email=data['email']).first():
                return jsonify({"message": "Email já cadastrado para outro restaurante"}), 409
            restaurante.email = data['email']

      
        if restaurante.endereco and any(f.startswith('endereco_') for f in data):
            restaurante.endereco.rua = data.get('endereco_rua', restaurante.endereco.rua)
            restaurante.endereco.numero = data.get('endereco_numero', restaurante.endereco.numero)
            restaurante.endereco.complemento = data.get('endereco_complemento', restaurante.endereco.complemento)
            restaurante.endereco.bairro = data.get('endereco_bairro', restaurante.endereco.bairro)
            restaurante.endereco.cidade = data.get('endereco_cidade', restaurante.endereco.cidade)
            restaurante.endereco.estado = data.get('endereco_estado', restaurante.endereco.estado)
            restaurante.endereco.cep = data.get('endereco_cep', restaurante.endereco.cep)
        elif not restaurante.endereco and any(f.startswith('endereco_') for f in data):
       
            novo_endereco = Endereco(
                rua=data.get('endereco_rua'), numero=data.get('endereco_numero'),
                complemento=data.get('endereco_complemento'), bairro=data.get('endereco_bairro'),
                cidade=data.get('endereco_cidade'), estado=data.get('endereco_estado'),
                cep=data.get('endereco_cep')
            )
            db.session.add(novo_endereco)
            restaurante.endereco = novo_endereco


        db.session.commit()
        return jsonify(serialize_restaurante(restaurante)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar restaurante", "error": str(e)}), 500

# ROTA PARA DELETAR UM RESTAURANTE (DELETE)
@restaurantes_bp.route('/<int:restaurante_id>', methods=['DELETE'])
def delete_restaurante(restaurante_id):
    restaurante = Restaurante.query.get(restaurante_id)
    if not restaurante:
        return jsonify({"message": "Restaurante não encontrado"}), 404

    try:
      
        if restaurante.endereco:
            db.session.delete(restaurante.endereco)
        
        db.session.delete(restaurante)
        db.session.commit()
        return jsonify({"message": "Restaurante excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao excluir restaurante", "error": str(e)}), 500