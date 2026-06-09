from sqlalchemy.orm import Session

from ..models import ItemLike, PlanLike
from .renovation_service import RenovationService


class LikeService:
    def __init__(self, db: Session):
        self.db = db

    def toggle_item_like(self, user_id: int, item_id: int) -> dict:
        existing = self.db.query(ItemLike).filter(
            ItemLike.user_id == user_id, ItemLike.item_id == item_id
        ).first()
        if existing:
            self.db.delete(existing)
            self.db.commit()
            return {"is_liked": False}
        self.db.add(ItemLike(user_id=user_id, item_id=item_id))
        self.db.commit()
        return {"is_liked": True}

    def toggle_plan_like(self, user_id: int, plan_id: int) -> dict:
        existing = self.db.query(PlanLike).filter(
            PlanLike.user_id == user_id, PlanLike.plan_id == plan_id
        ).first()
        renovation_svc = RenovationService(self.db)
        if existing:
            self.db.delete(existing)
            renovation_svc.decrement_likes(plan_id)
            self.db.commit()
            return {"is_liked": False}
        self.db.add(PlanLike(user_id=user_id, plan_id=plan_id))
        renovation_svc.increment_likes(plan_id)
        self.db.commit()
        return {"is_liked": True}

    def get_item_like_count(self, item_id: int) -> int:
        return self.db.query(ItemLike).filter(ItemLike.item_id == item_id).count()

    def get_plan_like_count(self, plan_id: int) -> int:
        return self.db.query(PlanLike).filter(PlanLike.plan_id == plan_id).count()

    def is_item_liked_by_user(self, user_id: int, item_id: int) -> bool:
        return self.db.query(ItemLike).filter(
            ItemLike.user_id == user_id, ItemLike.item_id == item_id
        ).first() is not None

    def is_plan_liked_by_user(self, user_id: int, plan_id: int) -> bool:
        return self.db.query(PlanLike).filter(
            PlanLike.user_id == user_id, PlanLike.plan_id == plan_id
        ).first() is not None
