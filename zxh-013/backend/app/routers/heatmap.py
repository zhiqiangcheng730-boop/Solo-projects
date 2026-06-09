from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import heatmap_service

router = APIRouter(prefix="/api/heatmap", tags=["heatmap"])


@router.get("")
def get_heatmap(
    south: float = Query(),
    north: float = Query(),
    east: float = Query(),
    west: float = Query(),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return heatmap_service.generate_heatmap(db, south, north, east, west, category=category)
