from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user_id
from ..schemas import MarkerCreate, MarkerOut
from ..services import marker_service

router = APIRouter(prefix="/api/markers", tags=["markers"])


@router.post("", response_model=MarkerOut)
def create_marker(data: MarkerCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return marker_service.create_marker(db, user_id, data)


@router.get("", response_model=list[MarkerOut])
def list_markers(
    south: float = Query(),
    north: float = Query(),
    east: float = Query(),
    west: float = Query(),
    category: str | None = Query(None),
    db: Session = Depends(get_db),
):
    if south > north or west > east:
        raise HTTPException(400, "Invalid bounds")
    return marker_service.get_markers_in_bounds(db, south, north, east, west, category)


@router.get("/{marker_id}", response_model=MarkerOut)
def get_marker(marker_id: int, db: Session = Depends(get_db)):
    m = marker_service.get_marker_by_id(db, marker_id)
    if not m:
        raise HTTPException(404, "Marker not found")
    return m
