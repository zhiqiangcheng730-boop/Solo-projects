from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    lat = Column(Float, default=0.0)
    lon = Column(Float, default=0.0)
    time_coins = Column(Integer, default=3)
    credit_score = Column(Float, default=100.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
