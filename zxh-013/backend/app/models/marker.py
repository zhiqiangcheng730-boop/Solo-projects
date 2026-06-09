from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from ..database import Base


class Marker(Base):
    __tablename__ = "markers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(32), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    description = Column(String(512), default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    vote_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
