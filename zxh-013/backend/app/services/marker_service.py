from sqlalchemy.orm import Session
from ..models.marker import Marker


def create_marker(db: Session, user_id: int, data) -> Marker:
    marker = Marker(user_id=user_id, **data.model_dump())
    db.add(marker)
    db.commit()
    db.refresh(marker)
    return marker


def get_markers_in_bounds(
    db: Session,
    south: float,
    north: float,
    east: float,
    west: float,
    category: str | None = None,
) -> list[Marker]:
    q = db.query(Marker).filter(
        Marker.latitude >= south,
        Marker.latitude <= north,
        Marker.longitude >= west,
        Marker.longitude <= east,
    )
    if category:
        q = q.filter(Marker.category == category)
    return q.order_by(Marker.created_at.desc()).limit(500).all()


def get_marker_by_id(db: Session, marker_id: int) -> Marker | None:
    return db.query(Marker).filter(Marker.id == marker_id).first()


def get_markers_by_user(db: Session, user_id: int) -> list[Marker]:
    return db.query(Marker).filter(Marker.user_id == user_id).order_by(Marker.created_at.desc()).all()
