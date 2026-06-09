from sqlalchemy.orm import Session
from ..models.subscription import Subscription
from ..models.marker import Marker
from ..utils import haversine


def create_subscription(db: Session, user_id: int, data) -> Subscription:
    sub = Subscription(user_id=user_id, **data.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def get_user_subscriptions(db: Session, user_id: int) -> list[Subscription]:
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()


def delete_subscription(db: Session, user_id: int, sub_id: int) -> bool:
    sub = (
        db.query(Subscription)
        .filter(Subscription.id == sub_id, Subscription.user_id == user_id)
        .first()
    )
    if not sub:
        return False
    db.delete(sub)
    db.commit()
    return True


def get_new_markers_for_subscription(db: Session, sub: Subscription, since_id: int = 0) -> list[Marker]:
    markers = (
        db.query(Marker)
        .filter(Marker.id > since_id)
        .order_by(Marker.created_at.desc())
        .limit(200)
        .all()
    )
    return [
        m for m in markers if haversine(sub.center_lat, sub.center_lng, m.latitude, m.longitude) <= sub.radius_km
    ]
