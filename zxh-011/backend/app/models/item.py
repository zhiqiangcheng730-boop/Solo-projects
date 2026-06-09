from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from ..database import Base


class ItemCategory(str, enum.Enum):
    CLOTHING = "clothing"
    FURNITURE = "furniture"
    ELECTRONICS = "electronics"
    PACKAGING = "packaging"


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    category = Column(SAEnum(ItemCategory), nullable=False)
    difficulty = Column(SAEnum(Difficulty), default=Difficulty.EASY)
    material = Column(String(100), default="")
    size_desc = Column(String(100), default="")
    image_url = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")  # pending / in_progress / completed
    creator_id = Column(Integer, index=True, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    progress_steps = relationship("ProgressStep", back_populates="item", order_by="ProgressStep.step_order")
    renovation_plans = relationship("RenovationPlan", back_populates="item")
