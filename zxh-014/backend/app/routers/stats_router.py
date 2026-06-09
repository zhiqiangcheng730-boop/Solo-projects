from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.stats_service import StatsService

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    summary = StatsService.get_summary(db)
    summary["top_keywords"] = StatsService.get_top_keywords(db, limit=30)
    summary["top_explanations"] = StatsService.get_top_explanations(db, limit=10)
    summary["emotion_correlations"] = StatsService.get_emotion_correlation(db)
    return summary


@router.get("/keywords/top")
def get_top_keywords(db: Session = Depends(get_db), limit: int = 30):
    return StatsService.get_top_keywords(db, limit)


@router.get("/explanations/top")
def get_top_explanations(db: Session = Depends(get_db), limit: int = 10):
    return StatsService.get_top_explanations(db, limit)


@router.get("/emotion-correlation")
def get_emotion_correlation(db: Session = Depends(get_db)):
    return StatsService.get_emotion_correlation(db)
