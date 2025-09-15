from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from app.auth import get_auth_user


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/", response_model=list[ReviewSchema],
            status_code=status.HTTP_200_OK)
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех отзывов.
    """
    result = await db.scalars(
        select(ReviewModel).where(ReviewModel.is_active == True))
    reviews = result.all()
    return reviews


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


@router.post("/", response_model=ReviewSchema,
             status_code=status.HTTP_201_CREATED)
async def create_reviews(review: ReviewCreate,
                         db: AsyncSession = Depends(get_async_db),
                         current_user: UserModel = Depends(get_auth_user)):
    """
    Создаёт новый отзыв.
    """
    result = await db.scalars(
        select(ProductModel).where(ProductModel.id == review.product_id,
                                   ProductModel.is_active == True)
        )
    product = result.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found or inactive")
    if review.grade <= 0 or review.grade > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The grade is out of range (1, 5)")
    db_review = ReviewModel(**review.model_dump(),
                            buyer_id=current_user.id,
                            comment_date=datetime.now())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)

    await update_product_rating(db, review.product_id)
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: UserModel = Depends(get_auth_user)):
    """
    Удаляет отзыв по его ID.
    """
    result_review = await db.scalars(
        select(ReviewModel).where(ReviewModel.id == review_id,
                                  ReviewModel.is_active == True)
    )
    review = result_review.first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Review not found or inactive")
    if review.buyer_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only delete your own review")
    await db.execute(
        update(ReviewModel).where(
            ReviewModel.id == review_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(review)
    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}
