from typing import Any

from sqlalchemy.orm import Session

from app.models import Categories


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, category_id: int) -> Categories | None:
        return (
            self.db.query(Categories)
            .filter(Categories.id == category_id)
            .first()
        )

    def get_by_name(self, name: str) -> Categories | None:
        return self.db.query(Categories).filter(Categories.name == name).first()

    def get_all(self) -> list[Categories]:
        return self.db.query(Categories).all()

    def create(self, category: Categories) -> Categories:
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Categories, dados: dict[str,Any]) -> Categories:
        for campo, valor in dados.items():
            setattr(category, campo, valor)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Categories) -> None:
        self.db.delete(category)
        self.db.commit()