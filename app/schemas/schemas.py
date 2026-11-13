from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import MovementType


class ProductCreateSchema(BaseModel):
    name: str = Field(..., max_length=150)
    sku: str = Field(..., max_length=50)
    price: Decimal = Field(..., ge=0)
    min_stock: int = 0
    max_stock: int = 0
    is_active: bool = True
    category_id: int


class ProductUpdateSchema(BaseModel):
    name: str | None = Field(default=None, max_length=150)
    sku: str | None = Field(default=None, max_length=50)
    price: Decimal | None = Field(default=None, ge=0)
    min_stock: int | None = None
    max_stock: int | None = None
    is_active: bool | None = None
    category_id: int | None = None


class ProductResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sku: str
    price: Decimal
    stock_quantity: int
    min_stock: int
    max_stock: int
    is_active: bool
    category_id: int
    created_at: datetime
    updated_at: datetime | None


class CategoryCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(default=None, max_length=255)


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class CategoryResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    created_at: datetime


class StockMovementCreateSchema(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: int = Field(..., ge=0)
    reason: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def require_reason_for_adjustment(self):
        if self.movement_type == MovementType.ADJUSTMENT and not (
            self.reason and self.reason.strip()
        ):
            raise ValueError("razão é obrigatório para ajustes de estoque")
        if self.movement_type != MovementType.ADJUSTMENT and self.quantity == 0:
            raise ValueError("A quantidade deve ser maior que zero")
        return self


class StockMovementResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    movement_type: MovementType
    quantity: int
    reason: str | None
    stock_before: int
    stock_after: int
    created_at: datetime
