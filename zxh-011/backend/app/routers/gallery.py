from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import GalleryService

router = APIRouter(prefix="/api/gallery", tags=["gallery"])


@router.get("/featured")
def get_featured(
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    svc = GalleryService(db)
    results, total = svc.get_featured(page, page_size)
    return {"items": results, "total": total, "page": page}


@router.get("/hot")
def get_hot(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    svc = GalleryService(db)
    return svc.get_hot_plans(limit)


@router.get("/plans/{plan_id}")
def get_plan_detail(plan_id: int, db: Session = Depends(get_db)):
    svc = GalleryService(db)
    detail = svc.get_plan_detail(plan_id)
    if detail is None:
        return {"error": "not found"}
    return detail
