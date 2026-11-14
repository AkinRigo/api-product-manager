<div align="center">

# 📦 Product Manager API

**Produtos, categorias e estoque em uma API simples, rápida e efetiva.**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/Licença-MIT-green)

</div>

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Principais funcionalidades](#-principais-funcionalidades)
- [Regras de negócio](#-regras-de-negócio)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração e instalação](#-configuração-e-instalação)
- [Documentação da API](#-documentação-da-api)
- [Frontend](#-frontend)
- [Endpoints](#-endpoints)
- [Banco de dados e migrations](#-banco-de-dados-e-migrations)
- [Testes](#-testes)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 📖 Sobre o projeto

A **Product Manager** foi criada para integrar sistemas que manuseiam produtos, suas categorias e estoques.

O objetivo principal é facilitar a operação com uma ferramenta simples de usar, construída em **FastAPI**. Em sistemas que tratam essas aplicações, geralmente se usam APIs externas ou se criam rotas dentro do próprio sistema. A Product Manager facilita essa integração de forma **simples, rápida e efetiva**.

---

## ✨ Principais funcionalidades

- Cadastrar, consultar, listar e atualizar **produtos**.
- Cadastrar, consultar, listar e atualizar **categorias**.
- Registrar **entradas, saídas e ajustes** de estoque.
- Consultar o histórico de movimentações de estoque.
- Consultar movimentações associadas a um produto.
- Filtrar produtos com estoque baixo.
- Acessar a documentação interativa da API pelo Swagger.

---

## 📋 Regras de negócio

### Produtos

- Nome, SKU, preço e categoria são obrigatórios.
- O SKU deve ser único.
- O preço não pode ser negativo; zero é permitido.
- Produtos inativos não podem receber entradas nem saídas de estoque. Ajustes continuam permitidos.
- Estoque baixo significa `stock_quantity <= min_stock`.

### Categorias

- Uma categoria pode ter vários produtos.
- O nome da categoria deve ser único.
- Não é possível excluir categorias em uso.

### Estoque

- Toda movimentação deve ter produto, tipo, quantidade e data; a data é gerada pelo sistema.
- Uma saída não pode exceder o saldo disponível, e o estoque nunca pode ficar negativo.
- Movimentações são transacionais.
- O motivo é obrigatório somente para `ADJUSTMENT`.
- `ENTRY` e `EXIT` precisam de quantidade maior que zero. Um `ADJUSTMENT` pode definir o saldo como zero.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| **Python** | Linguagem principal |
| **FastAPI** | Framework da API |
| **PostgreSQL** | Banco de dados |
| **SQLAlchemy** | ORM |
| **Alembic** | Migrations |
| **Pydantic** | Validação de dados |
| **Docker** | Containers da API e do banco |

---

## 🗂️ Estrutura do projeto

```text
product-manager-api/
├── alembic/
│   └── versions/
├── app/
│   ├── core/
│   │   └── database.py
│   ├── exceptions/
│   │   └── exceptions.py
│   ├── models/
│   │   └── models.py
│   ├── repositories/
│   │   ├── category_repository.py
│   │   ├── product_repository.py
│   │   └── stock_repository.py
│   ├── routers/
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── stock.py
│   ├── schemas/
│   │   └── schemas.py
│   └── services/
│       ├── category_service.py
│       ├── product_service.py
│       └── stock_service.py
├── tests/
│   ├── conftest.py
│   ├── test_categories.py
│   ├── test_models.py
│   ├── test_products.py
│   └── test_stock.py
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── main.py
├── pyproject.toml
└── README.md
```

### Pastas

| Pasta | Conteúdo |
|---|---|
| `app/` | Código principal da API |
| `app/core/` | Configurações essenciais, como a conexão e as sessões do banco de dados |
| `app/models/` | Modelos SQLAlchemy que representam as tabelas e os relacionamentos |
| `app/schemas/` | Schemas Pydantic para validar os dados recebidos e definir as respostas |
| `app/exceptions/` | Exceções da aplicação e regras para transformá-las em respostas HTTP |
| `app/routers/` | Endpoints da API, separados por categorias, produtos e estoque |
| `app/services/` | Regras de negócio e coordenação das operações |
| `app/repositories/` | Consultas e operações de persistência no banco de dados |
| `alembic/` | Migrations que registram e aplicam alterações na estrutura do banco |
| `tests/` | Testes automatizados. O `conftest.py` configura recursos compartilhados; os `test_*.py` testam modelos, categorias, produtos e estoque |

### Arquivos principais

| Arquivo | Função |
|---|---|
| `main.py` | Cria a aplicação FastAPI e registra as rotas |
| `alembic.ini` | Configura o Alembic |
| `docker-compose.yml` | Configura os containers da API e do PostgreSQL |
| `Dockerfile` | Define como construir a imagem da API |
| `.env` | Guarda configurações locais, como a URL do banco; **não deve ser compartilhado** |
| `.gitignore` | Lista arquivos que o Git deve ignorar |
| `.dockerignore` | Lista arquivos que não devem ser incluídos na imagem Docker |
| `pyproject.toml` | Define dependências e configurações do projeto |
| `openapi.json` | Especificação da API, que pode ser importada em ferramentas como o Postman |
| `LICENSE` | Termos de uso e distribuição do projeto |
| `README.md` | Documentação do projeto |

---

## ✅ Pré-requisitos

### 🐳 Para executar com Docker

- Git
- Docker Desktop com Docker Compose
- Acesso à internet para baixar as imagens e dependências

### 💻 Para executar localmente

- Git
- Python 3.12 ou superior
- PostgreSQL 16 ou superior
- Acesso à internet para instalar as dependências

### 🧪 Para testar a API

- Importar o `openapi.json` no Postman, ou
- Acessar a documentação Swagger pelo navegador.

---

## ⚙️ Configuração e instalação

### 1. Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Ele contém as configurações de conexão com o PostgreSQL e **não deve ser compartilhado nem enviado ao Git**.

```env
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_DB=product_manager

DATABASE_URL=postgresql+psycopg://seu_usuario:sua_senha@localhost:5433/product_manager
DATABASE_URL_DOCKER=postgresql+psycopg://seu_usuario:sua_senha@db:5432/product_manager
TEST_DATABASE_URL=postgresql+psycopg://seu_usuario:sua_senha@localhost:5433/product_manager_test
```

> ⚠️ Configure o arquivo `.env` antes de iniciar a aplicação.

### 2. Instalação local

Na pasta do projeto, crie e ative o ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### 3. Executando com Docker

Para iniciar a API e o PostgreSQL:

```bash
docker compose up --build -d
```

Com Docker, a aplicação fica disponível em **http://localhost:8000/docs**.

---

## 📚 Documentação da API

Acesse a documentação interativa (Swagger) em:

👉 **http://localhost:8000/docs**

---

## 🎨 Frontend

O frontend foi criado com auxílio de IA (Codex Luna), seguindo uma especificação técnica e referências visuais. Ele oferece uma interface web para visualizar e interagir com os dados da API.

### 🛠️ Tecnologias

- **React 18** e **TypeScript**
- **Vite** para desenvolvimento e build
- **CSS puro**, sem biblioteca visual externa
- **`fetch` nativo** para comunicação com a API
- **npm** para gerenciamento de dependências

A URL da API é configurada pela variável `VITE_API_URL`. Se ela não estiver definida, o frontend usa `http://localhost:8000`.

### ⚙️ Executar localmente

Com a API em execução, abra um terminal na pasta `frontend` e instale as dependências:

```bash
npm install
```

Inicie o servidor de desenvolvimento:

```bash
npm run dev
```

Acesse o endereço informado pelo Vite no terminal, normalmente **http://localhost:5173**.

### 📦 Build de produção

Para gerar os arquivos otimizados de produção:

```bash
npm run build
```

---

## 🔌 Endpoints

### Categorias

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/categories/` | Criar categoria |
| `GET` | `/categories/` | Listar categorias |
| `GET` | `/categories/{category_id}` | Consultar categoria |
| `PATCH` | `/categories/{category_id}` | Atualizar categoria |
| `DELETE` | `/categories/{category_id}` | Excluir categoria |

### Produtos

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/products/` | Criar produto |
| `GET` | `/products/` | Listar produtos; use `?low_stock=true` para filtrar estoque baixo |
| `GET` | `/products/{product_id}` | Consultar produto |
| `PATCH` | `/products/{product_id}` | Atualizar produto |
| `DELETE` | `/products/{product_id}` | Excluir produto |

### Estoque

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/stock/` | Registrar movimentação |
| `GET` | `/stock/` | Listar movimentações |
| `GET` | `/stock/{movement_id}` | Consultar movimentação |
| `GET` | `/stock/products/{product_id}` | Listar movimentações de um produto |

---

## 🗄️ Banco de dados e migrations

O projeto utiliza **PostgreSQL**. Configure no arquivo `.env` as credenciais e as URLs de conexão com o banco, sem compartilhá-lo.

Ao iniciar a aplicação com Docker Compose, as migrations são aplicadas automaticamente antes da API iniciar. Para aplicá-las manualmente com os containers em execução:

```bash
docker compose exec api alembic upgrade head
```

---

## 🧪 Testes

O projeto usa **pytest**. Em ambiente virtual, rode:

```bash
pytest -v   # saída detalhada
pytest -q   # resumo mais curto
```

### Categorias

| Cenário | Resultado esperado |
|---|---|
| Criar uma categoria e encontrá-la na listagem | `201`; depois `200` |
| Criar outra categoria com o mesmo nome | `409` |
| Excluir uma categoria com produtos vinculados | `409` |

### Produtos

| Cenário | Resultado esperado |
|---|---|
| Criar produto com categoria existente | `201`; resposta com o `category_id` enviado e `stock_quantity` igual a 0 |
| Repetir um SKU existente | `409` |
| Enviar preço negativo | `422` |
| Enviar preço igual a zero | `201` |
| Inativar com `PATCH` e `{"is_active": false}` | `200`; a consulta posterior mostra o produto inativo |
| `GET /products/?low_stock=true` | `200`; lista só produtos com saldo `<= min_stock` |

> ℹ️ Não há teste de exclusão de produto; o comportamento de `DELETE` ficou inalterado, como combinado.

### Estoque

| Cenário | Resultado esperado |
|---|---|
| Registrar `ENTRY`, `EXIT` e `ADJUSTMENT` válidos | `201` cada; a resposta mostra `stock_before`, `stock_after` e `reason`, e o saldo do produto reflete a movimentação |
| `ENTRY` ou `EXIT` sem `reason` | `201` (motivo opcional nesses tipos) |
| `ADJUSTMENT` sem motivo | `422` |
| Ajuste para saldo zero, com motivo | `201`; saldo final igual a 0 |
| Saída sem saldo suficiente | `409`; saldo inalterado |
| `ENTRY` ou `EXIT` em produto inativo | `409` |
| Duas saídas simultâneas para um saldo que só permite uma | uma `201`, outra `409`; saldo nunca negativo |

---

## 📄 Licença

Distribuído sob a **Licença MIT**. Confira o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Construído e desenvolvido por **Akin Rigo**.