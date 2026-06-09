import secrets
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AnonymousShare(Base):
    __tablename__ = "anonymous_shares"

    id = Column(Integer, primary_key=True, index=True)
    dream_id = Column(Integer, ForeignKey("dream_records.id"), nullable=False)
    share_token = Column(String(32), unique=True, nullable=False, index=True, default=lambda: secrets.token_hex(16))
    created_at = Column(DateTime, default=datetime.utcnow)

    dream = relationship("DreamRecord")
    comments = relationship("ShareComment", back_populates="share", cascade="all, delete-orphan")


class ShareComment(Base):
    __tablename__ = "share_comments"

    id = Column(Integer, primary_key=True, index=True)
    share_id = Column(Integer, ForeignKey("anonymous_shares.id"), nullable=False)
    user_id = Column(String(64), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    share = relationship("AnonymousShare", back_populates="comments")
