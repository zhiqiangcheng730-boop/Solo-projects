from collections import Counter
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.dream import DreamRecord, DreamKeyword
from app.models.symbol import Symbol, SymbolExplanation
from app.models.sharing import AnonymousShare


class StatsService:
    """Statistical analysis of dream data and emotion correlations."""

    @staticmethod
    def get_top_keywords(db: Session, limit: int = 20) -> list[dict]:
        rows = (
            db.query(
                DreamKeyword.keyword,
                func.sum(DreamKeyword.frequency).label("total"),
            )
            .group_by(DreamKeyword.keyword)
            .order_by(func.sum(DreamKeyword.frequency).desc())
            .limit(limit)
            .all()
        )
        total = sum(r.total for r in rows) or 1
        return [
            {"keyword": r.keyword, "count": r.total, "ratio": round(r.total / total, 4)}
            for r in rows
        ]

    @staticmethod
    def get_top_explanations(db: Session, limit: int = 10) -> list[dict]:
        explanations = (
            db.query(SymbolExplanation)
            .options(joinedload(SymbolExplanation.symbol), joinedload(SymbolExplanation.votes))
            .all()
        )
        result = [
            {
                "id": exp.id,
                "keyword": exp.symbol.keyword,
                "explanation": exp.explanation,
                "user_id": exp.user_id,
                "vote_count": exp.vote_count,
            }
            for exp in explanations
        ]
        result.sort(key=lambda x: x["vote_count"], reverse=True)
        return result[:limit]

    @staticmethod
    def get_emotion_correlation(db: Session) -> list[dict]:
        emotions = ["anxiety", "calm", "excited"]
        results = []
        for emotion in emotions:
            dream_ids = [
                r[0] for r in
                db.query(DreamRecord.id)
                .filter(DreamRecord.emotion == emotion)
                .all()
            ]
            if not dream_ids:
                results.append({"emotion": emotion, "dream_count": 0, "top_keywords": []})
                continue

            keyword_counts: Counter[str] = Counter()
            for dk in (
                db.query(DreamKeyword)
                .filter(DreamKeyword.dream_id.in_(dream_ids))
                .all()
            ):
                keyword_counts[dk.keyword] += dk.frequency

            all_keywords = db.query(func.sum(DreamKeyword.frequency)).scalar() or 1
            emotion_total = sum(keyword_counts.values()) or 1
            top = keyword_counts.most_common(10)

            results.append({
                "emotion": emotion,
                "dream_count": len(dream_ids),
                "top_keywords": [
                    {
                        "keyword": kw,
                        "count": cnt,
                        "emotion_ratio": round(cnt / emotion_total * 100, 1),
                        "global_ratio": round(
                            (db.query(func.sum(DreamKeyword.frequency))
                              .filter(DreamKeyword.keyword == kw)
                              .scalar() or 0)
                            / all_keywords * 100, 1
                        ),
                    }
                    for kw, cnt in top
                ],
            })
        return results

    @staticmethod
    def get_summary(db: Session) -> dict:
        return {
            "total_dreams": db.query(DreamRecord).count(),
            "total_symbols": db.query(Symbol).count(),
            "total_explanations": db.query(SymbolExplanation).count(),
            "total_shares": db.query(AnonymousShare).count(),
        }
