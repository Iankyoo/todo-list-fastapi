# 🚀 Fast Zero - API Assíncrona de Tarefas e Usuários

Uma API RESTful de alta performance projetada para o gerenciamento de usuários e tarefas (Todo-list). 

Construída com uma arquitetura **100% assíncrona**, esta aplicação foca em escalabilidade, segurança de dados e excelência técnica, servindo como um modelo de boas práticas no ecossistema moderno do Python.

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.133.1-00a393.svg)
![Coverage](https://img.shields.io/badge/coverage-100%25-success.svg)
![Security](https://img.shields.io/badge/security-pwdlib_hash-yellow.svg)
![Deploy](https://img.shields.io/badge/deploy-Fly.io-purple.svg)

## ✨ Principais Funcionalidades

* **Arquitetura Assíncrona (Async):** Totalmente desenvolvida com rotinas não-bloqueantes (`async/await`) utilizando o driver `asyncpg` para máxima performance de I/O no banco de dados.
* **Segurança Reforçada:** Criptografia robusta de senhas (password hashing) utilizando **pwdlib**.
Autenticação e Autorização blindadas via **JWT (JSON Web Tokens)**, garantindo isolamento de dados entre usuários.
* **Qualidade de Código (100% de Cobertura):** Bateria de testes unitários e de integração exaustivos com **pytest**, cobrindo cada linha e cenário de falha da aplicação.
* **Validação Rigorosa:** Tipagem estrita e validação automática de *payloads* de entrada e saída com **Pydantic**.
* **Gestão de Todo-List:** CRUD completo com paginação e filtros dinâmicos por título, descrição e estado da tarefa.
* **Persistência Relacional:** Modelagem de dados e migrações estruturadas com **SQLAlchemy 2.0** e **Alembic**, integrados ao **PostgreSQL**.

## 🛠️ Stack Tecnológica

**Back-end & Dados**
* [FastAPI](https://fastapi.tiangolo.com/) - Framework web
* [PostgreSQL](https://www.postgresql.org/) - Banco de Dados Relacional
* [SQLAlchemy 2.0](https://www.sqlalchemy.org/) + [Alembic](https://alembic.sqlalchemy.org/) - ORM e Migrations
* [Pydantic](https://docs.pydantic.dev/) - Validação e serialização de dados
* [pwdlib](https://github.com/frankie567/pwdlib) - Hashing de senhas seguro

**DevOps & Qualidade**
* [Docker](https://www.docker.com/) & Docker Compose - Containerização do ambiente
* [GitHub Actions](https://github.com/features/actions) - CI/CD pipeline
* [Fly.io](https://fly.io/) - Cloud hosting e deploy contínuo
* [Pytest](https://docs.pytest.org/) & [Factory-boy](https://factoryboy.readthedocs.io/) - Framework de testes e mock de dados
* [Poetry](https://python-poetry.org/) - Gerenciamento de dependências

## 🚦 Como rodar o projeto localmente

### Pré-requisitos
Certifique-se de ter o Docker e o Docker Compose instalados.

### Passos para Execução

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/fast_zero.git](https://github.com/seu-usuario/fast_zero.git)
   cd fast_zero

2. **Configure o ambiente:**
Crie um arquivo .env na raiz do projeto:
    ```bash
    DATABASE_URL=postgresql+asyncpg://app_user:app_password@fastzero_database:5432/app_db
    SECRET_KEY=sua_chave_secreta_jwt_super_segura
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

3. **Inicie os containers:**
O Docker Compose irá montar a imagem, subir o banco de dados e rodar as migrações automaticamente:
    ```bash
    docker-compose up --build

4. **Acesse a API:**
A documentação interativa (Swagger UI) estará disponível em: http://localhost:8000/docs

**Testes e Cobertura**
Para atestar a confiabilidade da API, execute os testes localmente via Poetry:       
    ```bash
    poetry install poetry run task test

A suíte validará regras de negócio, segurança dos tokens JWT, endpoints, paginação e falhas esperadas.

**Integração e Entrega Contínuas (CI/CD)**
O ciclo de vida da aplicação é automatizado via GitHub Actions. Toda alteração no código fonte aciona um fluxo que:

1. Constrói o ambiente e instala dependências.

2. Executa a suíte completa do pytest.

3. Valida a cobertura obrigatória de código.

4. Após aprovação, realiza o deploy direto na infraestrutura do Fly.io.

**Autor:**
**Ian Kiyoshi Kobayashi** Estudante de Análise e Desenvolvimento de Sistemas (ADS) na Faculdade Impacta e aspirante a Engenheiro de Software.

Desenvolvido com foco na aplicação real de conceitos avançados de engenharia de software e infraestrutura em nuvem.
