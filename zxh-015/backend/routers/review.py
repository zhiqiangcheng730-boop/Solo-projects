from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.review import ReviewCreate, ReviewResponse
from services.review_service import ReviewService

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("/", response_model=ReviewResponse)
def create_review(data: ReviewCreate, reviewer_id: int = Query(...), db: Session = Depends(get_db)):
    return ReviewService.create(db, reviewer_id, data)


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    return ReviewService.get_user_reviews(db, user_id)
