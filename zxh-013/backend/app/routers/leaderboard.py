from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import LeaderboardEntry
from ..services import leaderboard_service

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
def get_leaderboard(limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    return leaderboard_service.get_leaderboard(db, limit)
