from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.user import User
from ..models.marker import Marker


def get_leaderboard(db: Session, limit: int = 20) -> list[dict]:
    rows = (
        db.query(
            User.id,
            User.nickname,
            User.score,
            func.count(Marker.id).label("marker_count"),
        )
        .outerjoin(Marker, Marker.user_id == User.id)
        .group_by(User.id)
        .order_by(User.score.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "rank": i + 1,
            "user_id": row.id,
            "nickname": row.nickname or row.id,
            "score": row.score,
            "marker_count": row.marker_count,
        }
        for i, row in enumerate(rows)
    ]
