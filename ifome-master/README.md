# 🍔 iFome - Clone do iFood

iFome é um projeto de marketplace de restaurantes, inspirado em plataformas como o iFood. O objetivo é criar uma plataforma intuitiva onde usuários podem descobrir restaurantes locais e visualizar seus cardápios de forma simples e rápida.

Este repositório documenta o desenvolvimento do projeto para a disciplina de Desenvolvimento de Sistemas da Faculdade Impacta.  

---

## 🚀 Tecnologias
- Python 3.12
- HTML5
- Flask
- Flask SQLaclchemy
- SQLite (desenvolvimento)
- PostgreSQL/MySQL (produção)
- Tailwind
- Docker

---

## ⚙️ Como rodar o projeto

### 🔹 Opção 1: Rodar sem Docker
1. Clone o repositório:
   git clone https://github.com/DanDosSantos/ifome.git
   cd ifome

2. Criar o ambiente virtual:

- python -m venv .venv

3. Ative o ambiente virtual:

Linux/MacOS
- source .venv/bin/activate

Windows
- .venv\Scripts\activate

4. Instale as dependencias:
- pip install -r requirements.txt

5. Configure as variáveis de ambiente (crie um arquivo .env na raiz do projeto):
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta
GOOGLE_MAPS_API_KEY=sua_chave_aqui

6. Inicie o banco de dados:
flask db upgrade

7. Rode o projeto:
flask run

- Acesse em: http://localhost:8090

---

## 🐳 Como Rodar o Projeto com Docker
1. Clone o repositório:
   git clone https://github.com/DanDosSantos/ifome.git
   cd ifome

2. Crie o arquivo .env na raiz contendo:
FLASK_APP=src/app.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta
GOOGLE_MAPS_API_KEY=sua_chave_aqui

3. Contrua e rode os containers:
docker-compose up --build
ou
docker-compose up -d --build

4. O projeto estará disponível em:
http://localhost:8090