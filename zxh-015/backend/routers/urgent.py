from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas.skill import SkillResponse
from services.urgent_service import UrgentService

router = APIRouter(prefix="/api/urgent", tags=["urgent"])


@router.get("/", response_model=List[SkillResponse])
def get_urgent_needs(city: Optional[str] = None, db: Session = Depends(get_db)):
    return UrgentService.get_urgent_needs(db, city)


@router.put("/{skill_id}/mark", response_model=SkillResponse)
def mark_urgent(skill_id: int, user_id: int = Query(...), reason: str = Query(default=""), db: Session = Depends(get_db)):
    return UrgentService.mark_urgent(db, skill_id, user_id, reason)


@router.put("/{skill_id}/unmark", response_model=SkillResponse)
def unmark_urgent(skill_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return UrgentService.unmark_urgent(db, skill_id, user_id)
