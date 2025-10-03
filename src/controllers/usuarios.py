from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from src.models.usuarios_model import Usuarios
from src.validators.usuario_validator import validar_usuario
from config_db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import re
import os

# Importações SOMENTE para Google OAuth
# Remova 'import requests' se não estiver usando para outra coisa, para evitar conflitos.
# A importação correta para o Google é a seguinte:
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


usuarios_bp = Blueprint('usuarios', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@usuarios_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        telefone = request.form['telefone']
        
        telefone_limpo = re.sub(r'\D', '', telefone)
        
        erros = validar_usuario(nome, email, senha, confirmar_senha, telefone_limpo)
        
        # Verificações adicionais no banco de dados para email e telefone
        if Usuarios.query.filter_by(email=email).first():
            erros.append("Este e-mail já está cadastrado.")
        if Usuarios.query.filter_by(telefone=telefone_limpo).first():
            erros.append("Este telefone já está cadastrado.")

        if erros:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('usuarios.cadastro'))

        senha_hash = generate_password_hash(senha, method='pbkdf2:sha256') # Ajustado o método

        novo_usuario = Usuarios(
            nome = nome, 
            email = email, 
            senha = senha_hash, # Salva a senha hash
            telefone = telefone_limpo
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('usuarios.login'))
    
    return render_template('usuarios/cadastro.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form['identificador'] # Pode ser email ou telefone
        senha = request.form['senha']
        telefone_limpo = re.sub(r'\D', '', identificador) # Limpa se for telefone

        usuario = Usuarios.query.filter(
            or_(Usuarios.email == identificador, Usuarios.telefone == telefone_limpo)
        ).first()

        # Verifica se o usuário existe E se ele possui uma senha definida (não é um usuário de login social)
        if usuario and usuario.senha and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email # Adiciona email na sessão
            flash(f'Login realizado com sucesso! Bem-vindo, {usuario.nome.split()[0]}!', 'success')
            return redirect(url_for('home.index'))
        elif usuario and not usuario.senha: # Usuário existe mas não tem senha (provavelmente de login social)
            flash('Você se cadastrou usando o Google. Por favor, use o botão "Fazer Login com o Google" para entrar.', 'info')
            return redirect(url_for('usuarios.login'))
        else:
            flash('Email/Telefone ou senha inválidos. Tente novamente.', 'error')
            return redirect(url_for('usuarios.login'))

    return render_template('usuarios/login.html')

@usuarios_bp.route('/logout')
def logout():
    session.clear() # Limpa toda a sessão
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home.index'))

@usuarios_bp.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))
    
    usuario = Usuarios.query.get(session['usuario_id'])
    # Adicionando um fallback caso o usuário não seja encontrado por algum motivo
    if not usuario:
        flash('Usuário não encontrado.', 'error')
        session.clear()
        return redirect(url_for('usuarios.login'))
        
    return render_template('usuarios/perfil.html', usuario=usuario)

@usuarios_bp.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))

    usuario = Usuarios.query.get(session['usuario_id'])
    if not usuario:
        flash('Usuário não encontrado para edição.', 'error')
        session.clear()
        return redirect(url_for('usuarios.login'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        telefone_limpo = re.sub(r'\D', '', telefone)
        cep = request.form['cep']
        rua = request.form['endereco'] 
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']

        # TODO: adicionar validações mais robustas para o perfil


        email_existente = Usuarios.query.filter(Usuarios.email == email, Usuarios.id != usuario.id).first()
        if email_existente:
            flash("Este email já está em uso por outro usuário.", 'error')
            return redirect(url_for('usuarios.editar_perfil'))

        telefone_existente = Usuarios.query.filter(Usuarios.telefone == telefone_limpo, Usuarios.id != usuario.id).first()
        if telefone_existente:
            flash("Este telefone já está em uso por outro usuário.", 'error')
            return redirect(url_for('usuarios.editar_perfil'))

        usuario.nome = nome
        usuario.email = email
        usuario.telefone = telefone_limpo
        
        from src.models.endereco_model import Endereco
        if usuario.endereco is None:
            novo_endereco = Endereco(
                rua=rua,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep,
                usuario_id=usuario.id # Associa o endereço ao usuário
            )
            db.session.add(novo_endereco)
            usuario.endereco = novo_endereco # Relaciona o novo endereço ao usuário
        else:
            usuario.endereco.rua = rua
            usuario.endereco.numero = numero
            usuario.endereco.complemento = complemento
            usuario.endereco.bairro = bairro
            usuario.endereco.cidade = cidade
            usuario.endereco.estado = estado
            usuario.endereco.cep = cep

        db.session.commit()
        
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.perfil'))

    return render_template('usuarios/editar-perfil.html', usuario=usuario)

@usuarios_bp.route('/editar-endereco', methods=['GET', 'POST'])
def editar_endereco():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))

    usuario = Usuarios.query.get(session['usuario_id'])
    if not usuario:
        flash('Usuário não encontrado para edição de endereço.', 'error')
        session.clear()
        return redirect(url_for('usuarios.login'))

    if request.method == 'POST':
        rua = request.form['rua']
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']

        # TODO: adicionar validações mais robustas para o endereço

        from src.models.endereco_model import Endereco
        if usuario.endereco is None:
            novo_endereco = Endereco(
                rua=rua,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep,
                usuario_id=usuario.id # Associa o endereço ao usuário
            )
            db.session.add(novo_endereco)
            usuario.endereco = novo_endereco # Relaciona o novo endereço ao usuário
        else:
            usuario.endereco.rua = rua
            usuario.endereco.numero = numero
            usuario.endereco.complemento = complemento
            usuario.endereco.bairro = bairro
            usuario.endereco.cidade = cidade
            usuario.endereco.estado = estado
            usuario.endereco.cep = cep

        db.session.commit()
        
        flash('Endereço atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.perfil')) 

    return render_template('usuarios/endereco.html', usuario=usuario)

# Rota para login/cadastro via Google
@usuarios_bp.route('/google-login', methods=['POST'])
def google_login():
    """Rota para lidar com o login/cadastro via Google."""
    token = request.json.get('token')
    print(f"Requisição para /google-login recebida. Token: {token[:50]}..." if token else "Token não recebido.")

    if not token:
        flash('Token do Google não fornecido.', 'error')
        return jsonify({'success': False, 'message': 'Token do Google não fornecido.'}), 400

    try:
        google_client_id = current_app.config.get('GOOGLE_CLIENT_ID')
        
        if not google_client_id:
            print("ERRO CRÍTICO: GOOGLE_CLIENT_ID não configurado no aplicativo Flask.")
            flash('Erro de configuração: ID do Cliente Google não encontrado.', 'error')
            return jsonify({'success': False, 'message': 'Erro de configuração do servidor.'}), 500

        print(f"Tentando verificar token com GOOGLE_CLIENT_ID: {google_client_id}")
        
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), google_client_id)

        google_user_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo.get('picture') 
        usuario = Usuarios.query.filter_by(google_id=google_user_id).first()

        if not usuario:
            usuario = Usuarios.query.filter_by(email=email).first()
            if usuario:
                usuario.google_id = google_user_id
                if not usuario.profile_picture and picture: 
                    usuario.profile_picture = picture
                db.session.commit()
            else:
                
                novo_usuario = Usuarios(
                    nome=name, 
                    email=email, 
                    google_id=google_user_id, 
                    profile_picture=picture,
                    senha=None,
                    telefone=None 
                )
                db.session.add(novo_usuario)
                db.session.commit()
                usuario = novo_usuario 

        # Fazer login do usuário
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_email'] = usuario.email
        if usuario.profile_picture: # Guarda a foto na sessão se disponível
            session['usuario_picture'] = usuario.profile_picture
        
        flash(f'Bem-vindo(a), {usuario.nome.split()[0]}!', 'success')
        return jsonify({'success': True, 'redirect_url': url_for('home.index')})

    except ValueError as ve: # Capture ValueError especificamente para tokens inválidos
        print(f"Erro de verificação do token Google (ValueError): {ve}")
        flash('Não foi possível verificar sua conta Google. Token inválido ou expirado.', 'error')
        return jsonify({'success': False, 'message': 'Token Google inválido.'}), 401
    except Exception as e:
        flash('Ocorreu um erro inesperado ao fazer login com o Google.', 'error')
        print(f"Erro geral no Google Login: {e}") # Para depuração
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500