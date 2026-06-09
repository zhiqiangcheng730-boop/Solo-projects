from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user_id
from ..schemas import VoteCreate
from ..services import vote_service

router = APIRouter(prefix="/api/votes", tags=["votes"])


@router.post("")
def cast_vote(data: VoteCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    ok = vote_service.cast_vote(db, user_id, data.marker_id)
    if not ok:
        raise HTTPException(409, "Already voted")
    return {"status": "ok"}


@router.delete("/{marker_id}")
def unvote(marker_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    ok = vote_service.remove_vote(db, user_id, marker_id)
    if not ok:
        raise HTTPException(404, "Vote not found")
    return {"status": "ok"}


@router.get("/check/{marker_id}")
def check_vote(marker_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return {"voted": vote_service.has_voted(db, user_id, marker_id)}
