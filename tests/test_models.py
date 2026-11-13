
from app.models import Base
from app.core.database import sessionLocal
from app.models import Product


print("Models importados com sucesso!")

for tabela in Base.metadata.sorted_tables:
    print(f"Tabela: {tabela.name}")
    for coluna in tabela.columns:
        print(f"  - {coluna.name}: {coluna.type}")

print("Estrutura carregada com sucesso!")


db = sessionLocal()

# Puxa o primeiro produto cadastrado no banco de dados
produto = db.query(Product).first()

if produto:
    print(f"Produto encontrado: {produto.name}")

    # O teste real do relationship acontece exatamente nesta linha:
    # Se a configuração estiver correta, ele trará o nome da categoria automaticamente.
    print(f"Categoria vinculada: {produto.category.name}")
else:
    print("O banco está vazio. Cadastre uma categoria e um produto no banco para testar.")

db.close()