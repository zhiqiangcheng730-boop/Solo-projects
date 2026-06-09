from sqlalchemy.orm import Session

from ..models import ProgressStep
from ..schemas.progress import ProgressStepCreate


class ProgressService:
    def __init__(self, db: Session):
        self.db = db

    def add_step(self, data: ProgressStepCreate) -> ProgressStep:
        step = ProgressStep(**data.model_dump())
        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)
        return step

    def list_by_item(self, item_id: int) -> list[ProgressStep]:
        return self.db.query(ProgressStep) \
            .filter(ProgressStep.item_id == item_id) \
            .order_by(ProgressStep.step_order).all()

    def remove_step(self, step_id: int) -> bool:
        step = self.db.query(ProgressStep).filter(ProgressStep.id == step_id).first()
        if not step:
            return False
        self.db.delete(step)
        self.db.commit()
        return True
