from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user_id
from ..schemas import SubscriptionCreate, SubscriptionOut, NotificationOut
from ..services import subscription_service

router = APIRouter(prefix="/api/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscriptionOut)
def create_subscription(data: SubscriptionCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return subscription_service.create_subscription(db, user_id, data)


@router.get("", response_model=list[SubscriptionOut])
def list_subscriptions(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return subscription_service.get_user_subscriptions(db, user_id)


@router.delete("/{sub_id}")
def delete_subscription(sub_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    ok = subscription_service.delete_subscription(db, user_id, sub_id)
    if not ok:
        raise HTTPException(404, "Subscription not found")
    return {"status": "ok"}


@router.get("/notifications", response_model=list[NotificationOut])
def get_notifications(user_id: int = Depends(get_current_user_id), since_id: int = Query(0), db: Session = Depends(get_db)):
    subs = subscription_service.get_user_subscriptions(db, user_id)
    result = []
    seen = set()
    for sub in subs:
        markers = subscription_service.get_new_markers_for_subscription(db, sub, since_id)
        for m in markers:
            if m.id not in seen:
                seen.add(m.id)
                result.append({
                    "id": m.id,
                    "marker_id": m.id,
                    "marker_title": m.title,
                    "marker_category": m.category,
                    "latitude": m.latitude,
                    "longitude": m.longitude,
                    "created_at": m.created_at,
                })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return result[:50]
