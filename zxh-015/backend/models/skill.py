from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, func
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(10), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, default="")
    category = Column(String(50), nullable=False)
    tags = Column(Text, default="[]")
    city = Column(String(50), nullable=False)
    lat = Column(Float, default=0.0)
    lon = Column(Float, default=0.0)
    is_urgent = Column(Boolean, default=False)
    urgent_reason = Column(String(200), default="")
    urgent_deadline = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
