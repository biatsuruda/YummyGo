# 🍔 YummyGo - Clone do iFood

<p align="center">
  <img src="src/static/logo-transparente.png" alt="Logo YummyGo" width="250"/>
</p>

YummyGo é um projeto de marketplace de restaurantes, inspirado em plataformas como o iFood. O objetivo é criar uma plataforma intuitiva onde usuários podem descobrir restaurantes locais e visualizar seus cardápios de forma simples e rápida.

Este repositório documenta o desenvolvimento do projeto para a disciplina de Desenvolvimento de Sistemas da Faculdade Impacta.

---

## ✨ Funcionalidades (Exemplos - personalize com o que seu app faz)

* **Autenticação de Usuário:** Cadastro e Login tradicional (e com Google, em desenvolvimento).
* **Visualização de Restaurantes e Cardápios:** Navegue por uma seleção de restaurantes e seus respectivos menus.
* **Carrinho de Compras:** Adicione e remova itens, visualize o total do pedido.
* **Gestão de Perfil:** Atualize informações pessoais e endereços de entrega.
* **Pesquisa:** Encontre restaurantes ou pratos específicos.

---

## 🚀 Tecnologias

* **Backend:**
    * Python 3.12
    * Flask (framework web)
    * Flask-SQLAlchemy (ORM para interação com o banco de dados)
    * Flask-Migrate (para migrações de banco de dados)
    * Werkzeug (para segurança de senhas)
    * `python-dotenv` (para gerenciar variáveis de ambiente)
    * `google-auth-oauthlib`, `google-auth-httplib2`, `requests` (para integração com Google OAuth)
* **Frontend:**
    * HTML5
    * Tailwind CSS (framework de estilização)
    * JavaScript (para interatividade)
* **Banco de Dados:**
    * SQLite (para desenvolvimento local)
    * PostgreSQL / MySQL (recomendado para produção)
* **Containerização:**
    * Docker
    * Docker Compose

---

## ⚙️ Como rodar o projeto

### 📝 Pré-requisitos

Certifique-se de ter instalado em sua máquina:
* Python 3.12
* pip (gerenciador de pacotes do Python)
* Git
* (Opcional, para Docker) Docker e Docker Compose

### 🔹 Opção 1: Rodar sem Docker (Ambiente Virtual)

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/DanDosSantos/ifome.git](https://github.com/DanDosSantos/ifome.git)
    cd ifome
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv .venv
    ```
    * **No Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    * **No Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo chamado `.env` na **raiz** do projeto (na mesma pasta onde está o `app.py` e `requirements.txt`).
    Preencha-o com as seguintes informações:

    ```env
    FLASK_APP=src/app.py
    FLASK_ENV=development
    SECRET_KEY=sua_chave_secreta_aqui # Use uma string longa e aleatória para segurança
    GOOGLE_CLIENT_ID=seu_client_id_do_google.apps.googleusercontent.com # Necessário para o Google Login
    GOOGLE_MAPS_API_KEY=sua_chave_da_api_do_google_maps # Necessário para funcionalidades de mapa/endereço
    ```
    * **Importante:**
        * Para `SECRET_KEY`, gere uma string aleatória (ex: `python -c "import os; print(os.urandom(24).hex())"`).
        * `GOOGLE_CLIENT_ID` é obtido no Google Cloud Console, para a integração do Google Login.
        * `GOOGLE_MAPS_API_KEY` é obtida no Google Cloud Console, para funcionalidades de mapas (se aplicável ao seu projeto).

5.  **Inicialize o banco de dados:**
    ```bash
    flask db upgrade
    ```
    * Este comando criará o arquivo `ifome.db` no diretório `src/` e aplicará todas as migrações necessárias para configurar o esquema do banco de dados.

6.  **Rode o projeto:**
    ```bash
    flask run --host=0.0.0.0 --port=8090
    ```
    * **Nota:** O `flask run` por padrão usa a porta 5000. Se você quer que ele rode na porta 8090 (como sugerido), deve especificá-la.

7.  **Acesse a aplicação em seu navegador:**
    ```
    http://localhost:8090
    ```

---

## 🐳 Como Rodar o Projeto com Docker

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/DanDosSantos/ifome.git](https://github.com/DanDosSantos/ifome.git)
    cd ifome
    ```

2.  **Crie o arquivo `.env` na raiz do projeto:**
    Preencha-o com as variáveis de ambiente necessárias, conforme o passo 4 da Opção 1 (sem Docker):
    ```env
    FLASK_APP=src/app.py
    FLASK_ENV=development
    SECRET_KEY=sua_chave_secreta_aqui
    GOOGLE_CLIENT_ID=seu_client_id_do_google.apps.googleusercontent.com
    GOOGLE_MAPS_API_KEY=sua_chave_da_api_do_google_maps
    ```
    * **Observação:** O Docker Compose pode usar variáveis de ambiente diretamente do `.env`. Se você planeja usar um banco de dados diferente (PostgreSQL, MySQL) dentro do Docker, as variáveis de conexão com o banco de dados também precisarão ser configuradas aqui ou no `docker-compose.yml`.

3.  **Construa e execute os containers:**
    ```bash
    docker-compose up --build
    ```
    * Para rodar em segundo plano (detached mode):
        ```bash
        docker-compose up -d --build
        ```
    * Este comando construirá as imagens (se necessário), criará os serviços definidos no `docker-compose.yml` e os iniciará. A migração do banco de dados (passo `flask db upgrade`) **deve ser incorporada ao `Dockerfile` ou ao `entrypoint.sh`** para que o banco seja inicializado automaticamente dentro do container.

4.  **Acesse a aplicação em seu navegador:**
    ```
    http://localhost:8090
    ```

5.  **Para parar os containers (se rodou em segundo plano):**
    ```bash
    docker-compose down
    ```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Se você deseja contribuir, por favor, siga os seguintes passos:

1.  Faça um fork do projeto.
2.  Crie uma nova branch (`git checkout -b feature/minha-feature`).
3.  Faça suas alterações e commit (`git commit -m 'feat: Adiciona minha nova feature'`).
4.  Envie para a branch (`git push origin feature/minha-feature`).
5.  Abra um Pull Request.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.