# Product Manager API

Este README serve como guia rápido da estrutura do projeto e da responsabilidade de cada pasta e arquivo. O scaffold contém apenas a estrutura; a implementação da API será feita depois.

## Estrutura

```text
product-manager-api/
├── app/
│   ├── core/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── exceptions/
│   │   └── exceptions.py
│   ├── routers/
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── stock.py
│   ├── services/
│   │   ├── product_service.py
│   │   └── stock_service.py
│   └── repositories/
│       ├── category_repository.py
│       ├── product_repository.py
│       └── stock_repository.py
├── alembic/
├── tests/
│   ├── conftest.py
│   ├── test_products.py
│   └── test_stock.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## O que cada parte faz

### `app/`

Contém as partes organizadas da aplicação FastAPI.

- `main.py` (na raiz): cria a aplicação FastAPI e registra os routers.

### `app/core/`

- `database.py`: configura a conexão com o banco, o engine, as sessões e a dependência `get_db`.

### `app/models/`

- `models.py`: define os modelos/tabelas do banco: `Categories`, `Product` e `Stockmovement`.

### `app/schemas/`

- `schemas.py`: define os schemas Pydantic usados para validar dados de entrada e formatar respostas da API.

### `app/exceptions/`

- `exceptions.py`: reúne exceções específicas da aplicação e erros de negócio.

### `app/routers/`

Define as rotas HTTP da API. Os routers recebem as requisições e encaminham o trabalho para os services.

- `categories.py`: endpoints de categorias.
- `products.py`: endpoints de produtos.
- `stock.py`: endpoints de estoque e movimentações.

### `app/services/`

Implementa as **regras de negócio** e coordena as operações da aplicação, usando os repositories para acessar os dados.

- `product_service.py`: regras de negócio relacionadas a produtos.
- `stock_service.py`: regras de negócio relacionadas ao estoque e às movimentações.

### `app/repositories/`

Centraliza o acesso e as consultas ao banco de dados, separando persistência das regras de negócio.

- `category_repository.py`: operações de banco para categorias.
- `product_repository.py`: operações de banco para produtos.
- `stock_repository.py`: operações de banco para estoque e movimentações.

### `alembic/`

Guarda a configuração e as migrações do Alembic, usadas para versionar e atualizar a estrutura do banco de dados.

### `tests/`

Contém os testes automatizados da aplicação.

- `conftest.py`: configura fixtures e recursos compartilhados pelos testes.
- `test_products.py`: testa os endpoints e comportamentos relacionados a produtos.
- `test_stock.py`: testa os endpoints e comportamentos relacionados ao estoque.

### Arquivos da raiz

- `docker-compose.yml`: define os serviços locais em containers, incluindo a API e o PostgreSQL.
- `Dockerfile`: descreve como construir a imagem Docker da API.
- `requirements.txt`: lista as dependências Python do projeto.
- `.env`: guarda configurações e variáveis de ambiente, como parâmetros de conexão; não deve conter segredos versionados.
- `.gitignore`: impede que `.env`, ambientes virtuais e arquivos temporários sejam enviados ao Git.
- `README.md`: documentação de referência da estrutura e das responsabilidades de cada parte.
