from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    nickname = Column(String(64), default="")
    score = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
