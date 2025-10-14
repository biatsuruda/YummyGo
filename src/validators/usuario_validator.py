import re

def validar_usuario(nome, email, senha, confirmar_senha, telefone):
    erros = []

    if not nome or not email or not senha or not telefone:
        erros.append("Todos os campos são obrigatórios.")
    
    if len(nome.split()) < 2:
        erros.append("Digite seu nome completo.")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        erros.append("Email inválido.")
    
    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres.")
    if not re.search(r'[A-Z]', senha):
        erros.append("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r'[0-9]', senha):
        erros.append("A senha deve conter pelo menos um número.")
    if not re.search(r'[^A-Za-z0-9]', senha):
        erros.append("A senha deve conter pelo menos um caractere especial.")

    if senha != confirmar_senha:
        erros.append("As senhas não coincidem.")
    
    if not re.match(r"^\+?\d{10,15}$", telefone):
        erros.append("Telefone inválido. Deve conter apenas números e pode incluir o código do país.")
    
    return erros