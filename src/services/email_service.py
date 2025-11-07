"""
Serviço de E-mail

Centraliza a lógica de envio de e-mails usando o Flask-Mail.
"""
from src.extensions import mail
from flask_mail import Message
from flask import current_app, render_template

def send_email(subject, recipients, template_name, **kwargs):
    """
    Função genérica para enviar e-mails.
    
    :param subject: O assunto do e-mail.
    :param recipients: Lista de destinatários (ex: ['email@exemplo.com']).
    :param template_name: O nome do ficheiro .html em 'templates/email/'
    :param kwargs: Argumentos para passar ao template (ex: nome, codigo_otp).
    """
    try:
        # Configura o remetente a partir do .env (MAIL_USERNAME)
        sender = current_app.config['MAIL_USERNAME']
        
        # Cria a mensagem
        msg = Message(subject, sender=sender, recipients=recipients)
        
        # Renderiza o corpo do e-mail usando um template HTML
        # (Vamos criar este template a seguir)
        msg.html = render_template(f'email/{template_name}.html', **kwargs)
        
        # Envia o e-mail
        mail.send(msg)
        
        return True
    
    except Exception as e:
        # Regista o erro (importante em produção)
        print(f"Erro ao enviar e-mail: {e}")
        return False