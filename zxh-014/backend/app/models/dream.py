from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class DreamRecord(Base):
    __tablename__ = "dream_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), nullable=False, index=True)
    content = Column(Text, nullable=False)
    emotion = Column(String(16), nullable=True)  # anxiety, calm, excited
    created_at = Column(DateTime, default=datetime.utcnow)

    keywords = relationship("DreamKeyword", back_populates="dream", cascade="all, delete-orphan")


class DreamKeyword(Base):
    __tablename__ = "dream_keywords"

    id = Column(Integer, primary_key=True, index=True)
    dream_id = Column(Integer, ForeignKey("dream_records.id"), nullable=False)
    keyword = Column(String(32), nullable=False, index=True)
    frequency = Column(Integer, default=1)

    dream = relationship("DreamRecord", back_populates="keywords")
