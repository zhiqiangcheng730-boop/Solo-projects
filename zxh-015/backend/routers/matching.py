from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.skill import SkillResponse
from services.matching_service import MatchingService

router = APIRouter(prefix="/api/matching", tags=["matching"])


@router.get("/skill/{skill_id}", response_model=List[SkillResponse])
def match_skill(skill_id: int, limit: int = 10, db: Session = Depends(get_db)):
    return MatchingService.match_for_skill(db, skill_id, limit)


@router.get("/recommendations/{user_id}", response_model=List[SkillResponse])
def get_recommendations(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    return MatchingService.get_recommendations(db, user_id, limit)
