from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from schemas.skill import SkillCreate, SkillResponse, SkillSearch
from services.skill_service import SkillService

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.post("/", response_model=SkillResponse)
def create_skill(data: SkillCreate, user_id: int = Query(...), db: Session = Depends(get_db)):
    return SkillService.create(db, user_id, data)


@router.get("/", response_model=List[SkillResponse])
def list_skills(
    city: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return SkillService.list_skills(db, city=city, skill_type=type, category=category, skip=skip, limit=limit)


@router.post("/search", response_model=List[SkillResponse])
def search_skills(filters: SkillSearch, db: Session = Depends(get_db)):
    return SkillService.search(db, filters)


@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    return SkillService.get_by_id(db, skill_id)


@router.delete("/{skill_id}")
def deactivate_skill(skill_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    SkillService.deactivate(db, skill_id, user_id)
    return {"message": "技能已下架"}


@router.put("/{skill_id}/urgent", response_model=SkillResponse)
def set_urgent(
    skill_id: int,
    user_id: int = Query(...),
    reason: str = Query(default=""),
    deadline: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    return SkillService.set_urgent(db, skill_id, user_id, reason, deadline)
