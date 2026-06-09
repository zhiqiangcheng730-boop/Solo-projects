from sqlalchemy.orm import Session
from app.models.symbol import Symbol, SymbolExplanation, ExplanationVote


class SymbolService:
    """Manage dream symbols and their crowd-sourced explanations."""

    @staticmethod
    def get_or_create_symbol(db: Session, keyword: str) -> Symbol:
        symbol = db.query(Symbol).filter(Symbol.keyword == keyword).first()
        if not symbol:
            symbol = Symbol(keyword=keyword)
            db.add(symbol)
            db.commit()
            db.refresh(symbol)
        return symbol

    @staticmethod
    def get_symbol_by_keyword(db: Session, keyword: str) -> Symbol | None:
        return db.query(Symbol).filter(Symbol.keyword == keyword).first()

    @staticmethod
    def symbol_exists(db: Session, symbol_id: int) -> bool:
        return db.query(Symbol).filter(Symbol.id == symbol_id).first() is not None

    @staticmethod
    def list_symbols(db: Session, skip: int = 0, limit: int = 100) -> list[Symbol]:
        return db.query(Symbol).offset(skip).limit(limit).all()

    @staticmethod
    def add_explanation(db: Session, symbol_id: int, user_id: str, explanation: str, source: str = "user") -> SymbolExplanation:
        entry = SymbolExplanation(
            symbol_id=symbol_id,
            user_id=user_id,
            explanation=explanation,
            source=source,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_explanations(db: Session, symbol_id: int) -> list[SymbolExplanation]:
        return (
            db.query(SymbolExplanation)
            .filter(SymbolExplanation.symbol_id == symbol_id)
            .order_by(SymbolExplanation.created_at.desc())
            .all()
        )

    @staticmethod
    def vote_explanation(db: Session, explanation_id: int, user_id: str) -> bool:
        existing = (
            db.query(ExplanationVote)
            .filter(
                ExplanationVote.explanation_id == explanation_id,
                ExplanationVote.user_id == user_id,
            )
            .first()
        )
        if existing:
            db.delete(existing)
            db.commit()
            return False
        vote = ExplanationVote(explanation_id=explanation_id, user_id=user_id)
        db.add(vote)
        db.commit()
        return True

    @staticmethod
    def get_top_explanations(db: Session, symbol_id: int, limit: int = 5) -> list[dict]:
        explanations = (
            db.query(SymbolExplanation)
            .filter(SymbolExplanation.symbol_id == symbol_id)
            .all()
        )
        result = []
        for exp in explanations:
            result.append({
                "id": exp.id,
                "user_id": exp.user_id,
                "explanation": exp.explanation,
                "source": exp.source,
                "vote_count": exp.vote_count,
                "created_at": exp.created_at,
            })
        result.sort(key=lambda x: x["vote_count"], reverse=True)
        return result[:limit]
