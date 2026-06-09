from typing import List
from sqlalchemy.orm import Session
from models.review import Review
from models.transaction import Transaction
from schemas.review import ReviewCreate
from services.user_service import UserService


class ReviewService:

    @staticmethod
    def create(db: Session, reviewer_id: int, data: ReviewCreate) -> Review:
        txn = db.query(Transaction).filter(Transaction.id == data.transaction_id).first()
        if not txn:
            raise ValueError("交易不存在")
        if txn.status != "completed":
            raise ValueError("交易未完成，无法评价")
        if reviewer_id not in (txn.from_user_id, txn.to_user_id):
            raise ValueError("无权评价该交易")
        existing = db.query(Review).filter(
            Review.transaction_id == data.transaction_id,
            Review.reviewer_id == reviewer_id,
        ).first()
        if existing:
            raise ValueError("已评价过该交易")
        reviewee_id = txn.to_user_id if reviewer_id == txn.from_user_id else txn.from_user_id
        review = Review(
            transaction_id=data.transaction_id,
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=data.rating,
            comment=data.comment,
        )
        db.add(review)
        UserService.update_credit_score(db, reviewee_id, data.rating)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_user_reviews(db: Session, user_id: int) -> List[Review]:
        return (
            db.query(Review)
            .filter(Review.reviewee_id == user_id)
            .order_by(Review.created_at.desc())
            .all()
        )
