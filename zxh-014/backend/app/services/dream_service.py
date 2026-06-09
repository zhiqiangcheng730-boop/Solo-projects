from sqlalchemy.orm import Session
from app.models.dream import DreamRecord, DreamKeyword
from app.services.keyword_extractor import KeywordExtractor
from app.services.symbol_service import SymbolService


class DreamService:
    """Encapsulates dream recording with keyword extraction."""

    @staticmethod
    def create(db: Session, user_id: str, content: str, emotion: str | None) -> DreamRecord:
        dream = DreamRecord(user_id=user_id, content=content, emotion=emotion)
        db.add(dream)
        db.flush()

        for kw in KeywordExtractor.extract(content):
            db.add(DreamKeyword(dream_id=dream.id, keyword=kw["keyword"], frequency=kw["frequency"]))
            SymbolService.get_or_create_symbol(db, kw["keyword"])

        db.commit()
        db.refresh(dream)
        return dream

    @staticmethod
    def list_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 50) -> list[DreamRecord]:
        return (
            db.query(DreamRecord)
            .filter(DreamRecord.user_id == user_id)
            .order_by(DreamRecord.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, dream_id: int) -> DreamRecord | None:
        return db.query(DreamRecord).filter(DreamRecord.id == dream_id).first()
