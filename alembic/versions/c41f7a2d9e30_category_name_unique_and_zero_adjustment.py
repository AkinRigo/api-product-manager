"""Make category names unique and allow zero stock adjustments."""

from typing import Sequence, Union

from alembic import op


revision: str = "c41f7a2d9e30"
down_revision: Union[str, Sequence[str], None] = "bd0772cf42ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_category_name", "category", ["name"])
    op.drop_constraint(
        "stock_movement_quantity_positive",
        "stock_movements",
        type_="check",
    )
    op.create_check_constraint(
        "stock_movement_quantity_positive",
        "stock_movements",
        "quantity >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "stock_movement_quantity_positive",
        "stock_movements",
        type_="check",
    )
    op.create_check_constraint(
        "stock_movement_quantity_positive",
        "stock_movements",
        "quantity > 0",
    )
    op.drop_constraint("uq_category_name", "category", type_="unique")
