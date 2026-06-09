from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String(32), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    explanations = relationship("SymbolExplanation", back_populates="symbol", cascade="all, delete-orphan")


class SymbolExplanation(Base):
    __tablename__ = "symbol_explanations"

    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    user_id = Column(String(64), nullable=False, index=True)
    explanation = Column(Text, nullable=False)
    source = Column(String(16), default="user")  # user, system
    created_at = Column(DateTime, default=datetime.utcnow)

    symbol = relationship("Symbol", back_populates="explanations")
    votes = relationship("ExplanationVote", back_populates="explanation", cascade="all, delete-orphan")

    @property
    def vote_count(self):
        return len(self.votes) if self.votes else 0


class ExplanationVote(Base):
    __tablename__ = "explanation_votes"

    id = Column(Integer, primary_key=True, index=True)
    explanation_id = Column(Integer, ForeignKey("symbol_explanations.id"), nullable=False)
    user_id = Column(String(64), nullable=False, index=True)

    explanation = relationship("SymbolExplanation", back_populates="votes")
