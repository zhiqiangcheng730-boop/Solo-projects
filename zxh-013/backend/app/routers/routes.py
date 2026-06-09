from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import RouteRequest, RouteResponse
from ..services import route_service

router = APIRouter(prefix="/api/route", tags=["route"])


@router.post("/optimize", response_model=RouteResponse)
def optimize_route(data: RouteRequest, db: Session = Depends(get_db)):
    return route_service.optimize_route(db, data.start_lat, data.start_lng, data.end_lat, data.end_lng)
