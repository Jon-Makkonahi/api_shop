from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Boolean, Text, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.database import Base
if TYPE_CHECKING:
    from .products import Product


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                   default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    grade: Mapped[int] = mapped_column(Integer, default=1)

    # связь один ко многим с таблице Продукты (один продукт - отзывы)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship(back_populates="reviews")

    # связь один ко многим с таблице Пользователь (один пользователь - отзывы)
    buyer_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    buyer = relationship("User", back_populates="reviews")
