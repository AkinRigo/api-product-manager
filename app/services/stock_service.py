from typing import Any

from sqlalchemy.orm import Session

from app.exceptions import (
    InactiveProductError,
    InsufficientStockError,
    StockMovementNotFoundError,
    StockProductNotFoundError,
)
from app.models import MovementType, Product, Stockmovement
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_repository import StockRepository


class StockService:
    def __init__(self, db: Session):
        self.db = db
        self.product_repository = ProductRepository(db)
        self.repository = StockRepository(db)

    def create(self, dados: dict[str, Any]) -> Stockmovement:
        produto = self.product_repository.get_by_id_for_update(dados["product_id"])
        if produto is None:
            raise StockProductNotFoundError("Produto não encontrado")

        tipo = MovementType(dados["movement_type"])
        quantidade = dados["quantity"]
        if quantidade < 0 or (
            quantidade == 0 and tipo != MovementType.ADJUSTMENT
        ):
            raise ValueError("A quantidade deve ser maior que zero")

        if not produto.is_active and tipo != MovementType.ADJUSTMENT:
            raise InactiveProductError(
                "Produto inativo não pode receber movimentações comuns"
            )

        motivo = dados.get("reason")
        if tipo == MovementType.ADJUSTMENT and not (motivo and motivo.strip()):
            raise ValueError("O motivo é obrigatório para ajustes")

        saldo_anterior = produto.stock_quantity
        if tipo == MovementType.ENTRY:
            saldo_posterior = saldo_anterior + quantidade
        elif tipo == MovementType.EXIT:
            saldo_posterior = saldo_anterior - quantidade
            if saldo_posterior < 0:
                raise InsufficientStockError("Estoque insuficiente para essa saída")
        else:
            saldo_posterior = quantidade

        produto.stock_quantity = saldo_posterior
        movimentacao = Stockmovement(
            **dados,
            stock_before=saldo_anterior,
            stock_after=saldo_posterior,
        )
        return self.repository.create(movimentacao)

    def get_by_id(self, movement_id: int) -> Stockmovement:
        movimentacao = self.repository.get_by_id(movement_id)
        if movimentacao is None:
            raise StockMovementNotFoundError("Movimentação não encontrada")
        return movimentacao

    def get_all(self) -> list[Stockmovement]:
        return self.repository.get_all()

    def get_by_product_id(self, product_id: int) -> list[Stockmovement]:
        if self.product_repository.get_by_id(product_id) is None:
            raise StockProductNotFoundError("Produto não encontrado")
        return self.repository.get_by_product_id(product_id)