from sqlalchemy.orm import Session

from app.models import Stockmovement


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, movement_id: int) -> Stockmovement | None:
        return (
            self.db.query(Stockmovement)
            .filter(Stockmovement.id == movement_id)
            .first()
        )

    def get_by_product_id(self, product_id: int) -> list[Stockmovement]:
        return (
            self.db.query(Stockmovement)
            .filter(Stockmovement.product_id == product_id)
            .order_by(Stockmovement.id)
            .all()
        )

    def get_all(self) -> list[Stockmovement]:
        return self.db.query(Stockmovement).order_by(Stockmovement.id).all()

    def create(self, movement: Stockmovement) -> Stockmovement:
        self.db.add(movement)
        self.db.commit()
        self.db.refresh(movement)
        return movement