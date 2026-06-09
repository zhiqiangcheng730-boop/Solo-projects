from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, UniqueConstraint
from ..database import Base


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = (UniqueConstraint("user_id", "marker_id", name="uq_user_marker_vote"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    marker_id = Column(Integer, ForeignKey("markers.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
