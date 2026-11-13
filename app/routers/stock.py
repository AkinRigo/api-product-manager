from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import StockMovementCreateSchema, StockMovementResponseSchema
from app.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.post(
    "/",
    response_model=StockMovementResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_stock_movement(
    dados: StockMovementCreateSchema,
    db: Session = Depends(get_db),
):
    return StockService(db).create(dados.model_dump())


@router.get("/", response_model=list[StockMovementResponseSchema])
def list_stock_movements(db: Session = Depends(get_db)):
    return StockService(db).get_all()


@router.get(
    "/products/{product_id}",
    response_model=list[StockMovementResponseSchema],
)
def list_product_stock_movements(product_id: int, db: Session = Depends(get_db)):
    return StockService(db).get_by_product_id(product_id)


@router.get("/{movement_id}", response_model=StockMovementResponseSchema)
def get_stock_movement(movement_id: int, db: Session = Depends(get_db)):
    return StockService(db).get_by_id(movement_id)