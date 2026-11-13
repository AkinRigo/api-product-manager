from sqlalchemy.orm import Session

from app.exceptions import (
    CategoryInUseError,
    CategoryNameAlreadyExistsError,
    CategoryNotFoundError,
)
from app.models import Categories
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create(self, dados: dict) -> Categories:
        if self.repository.get_by_name(dados["name"]):
            raise CategoryNameAlreadyExistsError("Esse nome de categoria já está em uso")
        categoria = Categories(**dados)
        return self.repository.create(categoria)

    def get_by_id(self, category_id: int) -> Categories:
        categoria = self.repository.get_by_id(category_id)
        if categoria is None:
            raise CategoryNotFoundError("Categoria não encontrada")
        return categoria

    def get_all(self) -> list[Categories]:
        return self.repository.get_all()

    def update(self, category_id: int, dados: dict) -> Categories:
        categoria = self.get_by_id(category_id)
        if "name" in dados:
            outra_categoria = self.repository.get_by_name(dados["name"])
            if outra_categoria is not None and outra_categoria.id != category_id:
                raise CategoryNameAlreadyExistsError(
                    "Esse nome de categoria já está em uso"
                )
        return self.repository.update(categoria, dados)

    def delete(self, category_id: int) -> None:
        categoria = self.get_by_id(category_id)
        if categoria.products:
            raise CategoryInUseError(
                "Não é possível excluir uma categoria que possui produtos"
            )
        self.repository.delete(categoria)