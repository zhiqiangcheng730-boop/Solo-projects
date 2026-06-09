from sqlalchemy.orm import Session

from ..models import RenovationPlan
from ..schemas.renovation import RenovationPlanCreate


class RenovationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: RenovationPlanCreate) -> RenovationPlan:
        plan = RenovationPlan(**data.model_dump())
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def get(self, plan_id: int) -> RenovationPlan | None:
        return self.db.query(RenovationPlan).filter(RenovationPlan.id == plan_id).first()

    def list_by_item(self, item_id: int) -> list[RenovationPlan]:
        return self.db.query(RenovationPlan) \
            .filter(RenovationPlan.item_id == item_id) \
            .order_by(RenovationPlan.likes_count.desc()).all()

    def increment_likes(self, plan_id: int) -> RenovationPlan | None:
        plan = self.get(plan_id)
        if plan:
            plan.likes_count += 1
            self.db.commit()
            self.db.refresh(plan)
        return plan

    def decrement_likes(self, plan_id: int) -> RenovationPlan | None:
        plan = self.get(plan_id)
        if plan and plan.likes_count > 0:
            plan.likes_count -= 1
            self.db.commit()
            self.db.refresh(plan)
        return plan
