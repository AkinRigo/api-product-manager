from enum import Enum as PyEnum
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean, ForeignKey, Enum as SqlEnum, \
    CheckConstraint, UniqueConstraint
import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer,nullable=False)
    min_stock = Column(Integer, default=0)
    max_stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime)
    category = relationship("Categories", back_populates="products")



class Categories(Base):
    __tablename__ = 'category'
    __table_args__ = (UniqueConstraint("name", name="uq_category_name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    products = relationship("Product", back_populates="category")


class MovementType(str, PyEnum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    ADJUSTMENT = "ADJUSTMENT"

class Stockmovement(Base):
    __tablename__ = 'stock_movements'


    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    movement_type = Column(
        "type",
        SqlEnum(MovementType, name="stock_movement_type"),
        nullable=False
    )
    quantity = Column(Integer, nullable=False)
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="stock_movement_quantity_positive"),
    )
    reason = Column(String(255), nullable=True)
    stock_before = Column(Integer, default=0)
    stock_after = Column(Integer, default=0)
    created_at = Column (DateTime, default=datetime.datetime.now)
