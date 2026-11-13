from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CategoryUpdateSchema,
)
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    dados: CategoryCreateSchema,
    db: Session = Depends(get_db),
):
    return CategoryService(db).create(dados.model_dump())


@router.get("/", response_model=list[CategoryResponseSchema])
def list_categories(db: Session = Depends(get_db)):
    return CategoryService(db).get_all()


@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return CategoryService(db).get_by_id(category_id)


@router.patch("/{category_id}", response_model=CategoryResponseSchema)
def update_category(
    category_id: int,
    dados: CategoryUpdateSchema,
    db: Session = Depends(get_db),
):
    return CategoryService(db).update(
        category_id,
        dados.model_dump(exclude_unset=True),
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    CategoryService(db).delete(category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)