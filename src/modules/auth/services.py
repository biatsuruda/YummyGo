"""
Serviços do Módulo de Autenticação

Este ficheiro contém a lógica de negócio (regras) 
separada das rotas (controllers).
"""
from src.extensions import db
from src.models import User
import random
import datetime
from src.services.email_service import send_email
from src.services.sms_service import send_sms

def create_new_user(nome_completo, email, telefone, password):
    """
    Cria um novo utilizador, encripta a senha e guarda na DB.
    Retorna o utilizador criado.
    """
    
    # 1. Cria a instância do novo utilizador
    # (Note que não passamos a password diretamente)
    new_user = User(
        nome_completo=nome_completo,
        email=email,
        telefone=telefone,
        role='cliente' # Define a 'role' padrão
    )
    
    # 2. Usa o método set_password (que definimos no user_model)
    #    para gerar e guardar o HASH da senha.
    new_user.set_password(password)
    
    # 3. Adiciona e 'commita' na base de dados
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        # Em caso de erro (ex: falha de 'unique'), faz rollback
        db.session.rollback()
        print(f"Erro ao criar utilizador: {e}") # Log do erro
        return None
    
def generate_and_send_otp(user):
    """
    Gera um OTP, guarda-o no utilizador e envia-o por e-mail.
    """
    try:
        # 1. Gerar Código
        # Gera um número entre 100000 e 999999 e converte para string
        otp_code = str(random.randint(100000, 999999))
        
        # 2. Definir Expiração (10 minutos a partir de agora)
        # O 'timezone.utc' garante que estamos a usar o tempo universal
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

        # 3. Salvar no Utilizador
        # (NÃO estamos a encriptar por agora, para ser mais simples)
        user.otp_code = otp_code
        user.otp_expiration = expiration_time
        
        db.session.commit()

        # 4. Enviar E-mail (Usando o nosso serviço!)
        success = send_email(
            subject="Seu Código de Acesso YummyGo",
            recipients=[user.email],
            template_name="otp_verification", # O template que já criámos
            nome=user.nome_completo,
            codigo_otp=otp_code
        )
        
        return success
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao gerar/enviar OTP: {e}")
        return False
    
def generate_and_send_sms_otp(user):
    """
    Gera um OTP, guarda-o no utilizador e envia-o por SMS.
    """
    try:
        # 1. Gerar Código (lógica idêntica à do e-mail)
        otp_code = str(random.randint(100000, 999999))
        
        # 2. Definir Expiração (10 minutos, naive UTC)
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)

        # 3. Salvar no Utilizador
        user.otp_code = otp_code
        user.otp_expiration = expiration_time
        
        db.session.commit()

        # 4. Enviar SMS (Usando o nosso serviço!)
        body = f"O seu código de verificação YummyGo é: {otp_code}"
        
        # NOTA: Isto assume que user.telefone está no formato
        # E.164 (ex: +5511999999999) que o Twilio exige!
        success = send_sms(
            to_number=user.telefone,
            body=body
        )
        
        return success
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao gerar/enviar OTP por SMS: {e}")
        return False