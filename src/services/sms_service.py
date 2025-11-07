"""
Serviço de SMS

Centraliza a lógica de envio de SMS via Twilio.
"""
from twilio.rest import Client
from flask import current_app

def send_sms(to_number, body):
    """
    Envia um SMS usando as credenciais do Twilio.
    
    :param to_number: O número do destinatário (ex: '+5511999999999')
    :param body: O texto da mensagem.
    """
    try:
        # 1. Carrega as credenciais do config (que leu do .env)
        account_sid = current_app.config['TWILIO_ACCOUNT_SID']
        auth_token = current_app.config['TWILIO_AUTH_TOKEN']
        from_number = current_app.config['TWILIO_PHONE_NUMBER']
        
        # 2. Cria o cliente Twilio
        client = Client(account_sid, auth_token)
        
        # 3. Cria e envia a mensagem
        message = client.messages.create(
            body=body,
            from_=from_number,  # O número de teste do Twilio
            to=to_number        # O número verificado do destinatário
        )
        
        # Log de sucesso (vemos isto no terminal)
        print(f"SMS enviado com sucesso! SID: {message.sid}")
        return True
    
    except Exception as e:
        # Log de erro
        print(f"Erro ao enviar SMS via Twilio: {e}")
        return False