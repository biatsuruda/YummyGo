"""
Ponto de Entrada da Aplicação (Entry Point)

Este ficheiro é responsável por importar a factory 'create_app' 
de dentro do pacote 'src' e iniciar o servidor de desenvolvimento.

É este ficheiro que o 'flask run' procura (devido ao FLASK_APP=src).
"""

from src import create_app
<<<<<<< HEAD
=======
import os

# Cria a instância da aplicação
app = create_app()

# ✅ Define a URI do banco diretamente no app.config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yummygo.db'
>>>>>>> 9cd02bf (Atualiza templates HTML, estiliza cardápio e corrige rotas de produtos e pedidos)
from flask import request # <-- Verifique se request está importado
from src.extensions import db 
from src.models import Pedido 
import stripe

# Cria a instância da aplicação usando a factory
app = create_app()

# --- ROTA DO WEBHOOK (ISOLADA) ---
@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    """
    Rota chamada pelo servidor do Stripe para notificar eventos (pagamento aprovado).
    """
    # 1. Obter o Webhook Secret do app.config (carregado pela create_app)
    endpoint_secret = app.config['STRIPE_WEBHOOK_SECRET']
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    event = None
    
    # 2. Verifica a assinatura (Segurança)
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print(f'ERRO WEBOOK GERAL (Assinatura): {e}')
        return 'Bad Request: Invalid payload or signature', 400

    # 3. Processa o sucesso do Checkout
    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        pedido_id = session_data.get('client_reference_id') # A nossa chave mestra
        
        if pedido_id:
            # Precisa de contexto de app para DB
            with app.app_context(): 
                # 5. Encontra o pedido na DB
                pedido = Pedido.query.get(int(pedido_id))
                
                # 6. Atualiza o status do pedido
                if pedido and pedido.status == 'Pendente de Pagamento':
                    pedido.status = 'Recebido'
                    # commit AQUI: (A nossa lógica anterior falhava, pois 
                    # a variável 'db' não estava ligada corretamente dentro
                    # deste contexto de função, por isso usamos db.session.)
                    db.session.commit() 
                    print(f"✅ WEBHOOK: Pedido #{pedido_id} atualizado para RECEBIDO.")
                else:
                    # Se não encontrou o pedido ou já foi atualizado
                    print(f"WEBHOOK: Pedido #{pedido_id} não encontrado ou já processado.")

# --- INÍCIO DO BLOCO DE TESTE DE E-MAIL ---
import click
from src.services.email_service import send_email
from src.services.sms_service import send_sms

@app.cli.command("test-email")
@click.argument("recipient")
def test_email_command(recipient):
    """
    Envia um e-mail de teste para verificar a configuração.
    
    Como usar no terminal:
    flask test-email seu-email-de-teste@exemplo.com
    """
    print(f"A tentar enviar e-mail de teste para: {recipient}...")
    
    # Gera um código OTP falso para o template
    subject = "YummyGo - Teste de E-mail"
    template = "otp_verification" # Usa o nosso template
    
    success = send_email(
        subject=subject,
        recipients=[recipient],
        template_name=template,
        nome="Utilizador de Teste",
        codigo_otp="999111"
    )
    
    if success:
        print("✅ E-mail enviado com sucesso!")
    else:
        print("❌ Falha ao enviar e-mail. Verifique o log e o .env.")
# --- FIM DO BLOCO DE TESTE ---

# --- INÍCIO DO BLOCO DE TESTE DE SMS ---
@app.cli.command("test-sms")
@click.argument("to_number")
def test_sms_command(to_number):
    """
    Envia um SMS de teste para verificar a configuração do Twilio.
    
    COMO USAR NO TERMINAL:
    (Use o seu n. de telemóvel verificado, com código do país!)
    
    ex: flask test-sms +5511999999999
    """
    print(f"A tentar enviar SMS de teste para: {to_number}...")
    
    body = "Teste do YummyGo! Se recebeu isto, o Twilio está a funcionar."
    
    # Chama o nosso novo serviço
    success = send_sms(to_number, body)
    
    if success:
        print("✅ SMS enviado com sucesso!")
    else:
        print("❌ Falha ao enviar SMS. Verifique o log, o .env e se o n. está verificado no Twilio.")
# --- FIM DO BLOCO DE TESTE ---

if __name__ == '__main__':
    # Permite executar o ficheiro diretamente com 'python run.py'
    # app.run() irá usar as configurações do FLASK_DEBUG (definido no .flaskenv)
    app.run()