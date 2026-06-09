from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from services.location_service import LocationService

router = APIRouter(prefix="/api/location", tags=["location"])


@router.get("/nearby")
def get_nearby(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float = 10.0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return LocationService.get_nearby_providers(db, lat, lon, radius_km, limit)


@router.get("/city/{city}")
def get_city_skills(city: str, db: Session = Depends(get_db)):
    return LocationService.get_city_skills(db, city)
