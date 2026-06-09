from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.like import LikeToggle
from ..services import LikeService

router = APIRouter(prefix="/api/likes", tags=["likes"])


@router.post("/item/toggle")
def toggle_item_like(data: LikeToggle, db: Session = Depends(get_db)):
    svc = LikeService(db)
    return svc.toggle_item_like(data.user_id, data.target_id)


@router.post("/plan/toggle")
def toggle_plan_like(data: LikeToggle, db: Session = Depends(get_db)):
    svc = LikeService(db)
    return svc.toggle_plan_like(data.user_id, data.target_id)


@router.get("/item/{item_id}")
def get_item_likes(item_id: int, user_id: int, db: Session = Depends(get_db)):
    svc = LikeService(db)
    return {
        "count": svc.get_item_like_count(item_id),
        "is_liked": svc.is_item_liked_by_user(user_id, item_id),
    }


@router.get("/plan/{plan_id}")
def get_plan_likes(plan_id: int, user_id: int, db: Session = Depends(get_db)):
    svc = LikeService(db)
    return {
        "count": svc.get_plan_like_count(plan_id),
        "is_liked": svc.is_plan_liked_by_user(user_id, plan_id),
    }
