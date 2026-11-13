from typing import Any

from sqlalchemy.orm import Session

from app.exceptions import (
    ProductCategoryNotFoundError,
    ProductNotFoundError,
    ProductSkuAlreadyExistsError,
)
from app.models import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    def create(self, dados: dict[str, Any]) -> Product:
        self._validate_product_data(dados)
        produto = Product(**dados, stock_quantity=0)
        return self.repository.create(produto)

    def get_by_id(self, product_id: int) -> Product:
        produto = self.repository.get_by_id(product_id)
        if produto is None:
            raise ProductNotFoundError("Produto não encontrado")
        return produto

    def get_all(self, low_stock: bool = False) -> list[Product]:
        if low_stock:
            return self.repository.get_low_stock()
        return self.repository.get_all()

    def update(self, product_id: int, dados: dict[str, Any]) -> Product:
        produto = self.get_by_id(product_id)
        self._validate_product_data(dados, product_id)
        return self.repository.update(produto, dados)

    def delete(self, product_id: int) -> None:
        produto = self.get_by_id(product_id)
        self.repository.delete(produto)

    def _validate_product_data(
        self,
        dados: dict[str, Any],
        product_id: int | None = None,
    ) -> None:
        if "price" in dados and dados["price"] < 0:
            raise ValueError("O preço não pode ser negativo")

        if "sku" in dados:
            produto = self.repository.get_by_sku(dados["sku"])
            if produto is not None and produto.id != product_id:
                raise ProductSkuAlreadyExistsError("Esse SKU já está em uso")

        if "category_id" in dados:
            categoria = self.category_repository.get_by_id(dados["category_id"])
            if categoria is None:
                raise ProductCategoryNotFoundError("Categoria não encontrada")