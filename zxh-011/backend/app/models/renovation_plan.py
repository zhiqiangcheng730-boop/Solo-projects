from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from ..database import Base


class RenovationPlan(Base):
    __tablename__ = "renovation_plans"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    reference_image_url = Column(String(500), default="")
    result_image_url = Column(String(500), default="")
    author_id = Column(Integer, index=True, default=0)
    likes_count = Column(Integer, default=0)
    is_featured = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    item = relationship("Item", back_populates="renovation_plans")
