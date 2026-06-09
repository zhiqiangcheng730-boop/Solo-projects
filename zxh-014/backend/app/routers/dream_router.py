from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import DreamCreate, DreamResponse
from app.services.dream_service import DreamService

router = APIRouter(prefix="/api/dreams", tags=["dreams"])


@router.post("", response_model=DreamResponse)
def create_dream(payload: DreamCreate, db: Session = Depends(get_db)):
    return DreamService.create(db, payload.user_id, payload.content, payload.emotion)


@router.get("", response_model=list[DreamResponse])
def list_dreams(user_id: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return DreamService.list_by_user(db, user_id, skip, limit)


@router.get("/{dream_id}", response_model=DreamResponse)
def get_dream(dream_id: int, db: Session = Depends(get_db)):
    return DreamService.get_by_id(db, dream_id)
