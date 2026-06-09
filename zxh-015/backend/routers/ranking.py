from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from services.ranking_service import RankingService

router = APIRouter(prefix="/api/ranking", tags=["ranking"])


@router.get("/helpers")
def get_top_helpers(limit: int = 20, db: Session = Depends(get_db)):
    return RankingService.get_top_helpers(db, limit)


@router.get("/credit")
def get_highest_credit(limit: int = 20, db: Session = Depends(get_db)):
    return RankingService.get_highest_credit(db, limit)
