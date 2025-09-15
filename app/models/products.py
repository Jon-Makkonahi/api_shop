from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Float, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base
if TYPE_CHECKING:
    from .categories import Category
    from .reviews import Review


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # связь один ко многим с таблице Категория (одна категория - товары)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="products")

    # связь один ко многим с таблице Пользователь (один пользователь - товары)
    seller_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    seller = relationship("User", back_populates="products")

    rating: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="product")
