from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.usuarios_model import Usuarios
from src.validators.usuario_validator import validar_usuario
from config_db import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import or_
import re
import re
import os

usuarios_bp = Blueprint('usuarios', __name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))

@usuarios_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        senha_hash = generate_password_hash(senha)
        confirmar_senha = request.form['confirmar_senha']
        telefone = request.form['telefone']
        # Limpa o telefone, removendo tudo que não for dígito
        telefone_limpo = re.sub(r'\D', '', telefone)
        # Passa o telefone limpo para o validador
        erros = validar_usuario(nome, email, senha, confirmar_senha, telefone_limpo)
        if erros:
            for erro in erros:
                flash(erro, 'error')
            return redirect(url_for('usuarios.cadastro'))

        novo_usuario = Usuarios(
            nome = nome, 
            email = email, 
            senha = senha_hash, 
            telefone = telefone_limpo
        )
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect(url_for('usuarios.login'))
    
    return render_template('cadastro.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form['identificador']
        senha = request.form['senha']
        telefone_limpo = re.sub(r'\D', '', identificador)
        # Procura o usuário por email ou pelo telefone
        usuario = Usuarios.query.filter(
            or_(Usuarios.email == identificador, Usuarios.telefone == telefone_limpo)
        ).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            flash(f'Login realizado com sucesso! Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('home.index'))
        else:
            flash('Email/Telefone ou senha inválidos. Tente novamente.', 'error')
            return redirect(url_for('usuarios.login'))

    return render_template('login.html')

@usuarios_bp.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))
    
    usuario = Usuarios.query.get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)

@usuarios_bp.route('/editar-perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))

    usuario = Usuarios.query.get(session['usuario_id'])

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

        # TODO: adicionar validações mais robustas para o perfil, trazer os erros como no exemplo de cadastro
        # erros = []

        # if not nome or not email or not telefone:
        #     erros.append("Todos os campos são obrigatórios.")
        
        # if len(nome.split()) < 2:
        #     erros.append("Digite seu nome completo.")
        
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        #     erros.append("Email inválido.")

        # if not re.match(r"^\+?\d{10,15}$", telefone_limpo):
        #     erros.append("Telefone inválido. Deve conter apenas números e pode incluir o código do país.")

        # # Verifica se o email já está em uso por outro usuário
        # email_existente = Usuarios.query.filter(Usuarios.email == email, Usuarios.id != usuario.id).first()
        # if email_existente:
        #     erros.append("Este email já está em uso por outro usuário.")

        # # Verifica se o telefone já está em uso por outro usuário
        # telefone_existente = Usuarios.query.filter(Usuarios.telefone == telefone_limpo, Usuarios.id != usuario.id).first()
        # if telefone_existente:
        #     erros.append("Este telefone já está em uso por outro usuário.")

        # if erros:
        #     for erro in erros:
        #         flash(erro, 'error')
        #     return redirect(url_for('usuarios.editar_perfil'))

        usuario.nome = nome
        usuario.email = email
        usuario.telefone = telefone_limpo
        usuario.cep = cep
        if usuario.endereco is None:
            from src.models.endereco_model import Endereco
            novo_endereco = Endereco(
                rua=rua,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep
            )
            db.session.add(novo_endereco)
            db.session.commit()
            usuario.endereco = novo_endereco
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

    return render_template('editar-perfil.html', usuario=usuario)

@usuarios_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('home.index'))


@usuarios_bp.route('/editar-endereco', methods=['GET', 'POST'])
def editar_endereco():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('usuarios.login'))

    usuario = Usuarios.query.get(session['usuario_id'])

    if request.method == 'POST':
        rua = request.form['rua']
        numero = request.form['numero']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']

        # TODO: adicionar validações mais robustas para o endereço, trazer os erros como no exemplo de cadastro


        if usuario.endereco is None:
            from src.models.endereco_model import Endereco
            novo_endereco = Endereco(
                rua=rua,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                estado=estado,
                cep=cep
            )
            db.session.add(novo_endereco)
            db.session.commit()
            usuario.endereco = novo_endereco
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
        return redirect(url_for('usuarios.perfil'))  # Após salvar, redireciona para o perfil

    return render_template('endereco.html', usuario=usuario)  # aqui ele vai passar o usuário com o endereço (se existir)