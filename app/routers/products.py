from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    ProductCreateSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    dados: ProductCreateSchema,
    db: Session = Depends(get_db),
):
    return ProductService(db).create(dados.model_dump())


@router.get("/", response_model=list[ProductResponseSchema])
def list_products(
    low_stock: bool = False,
    db: Session = Depends(get_db),
):
    return ProductService(db).get_all(low_stock=low_stock)


@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService(db).get_by_id(product_id)


@router.patch("/{product_id}", response_model=ProductResponseSchema)
def update_product(
    product_id: int,
    dados: ProductUpdateSchema,
    db: Session = Depends(get_db),
):
    return ProductService(db).update(
        product_id,
        dados.model_dump(exclude_unset=True),
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    produto = db.query(Product).filter(Product.id == product_id).first()
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado",
        )

    db.delete(produto)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)