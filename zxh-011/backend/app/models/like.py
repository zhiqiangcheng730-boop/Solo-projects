from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone

from ..database import Base


class ItemLike(Base):
    __tablename__ = "item_likes"
    __table_args__ = (UniqueConstraint("user_id", "item_id", name="uq_user_item_like"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PlanLike(Base):
    __tablename__ = "plan_likes"
    __table_args__ = (UniqueConstraint("user_id", "plan_id", name="uq_user_plan_like"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("renovation_plans.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
