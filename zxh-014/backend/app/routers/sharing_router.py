from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import ShareCreate, ShareResponse, CommentCreate, CommentResponse
from app.services.sharing_service import SharingService

router = APIRouter(prefix="/api/shares", tags=["shares"])


@router.post("", response_model=ShareResponse)
def create_share(payload: ShareCreate, db: Session = Depends(get_db)):
    return SharingService.create_share_response(db, payload.dream_id)


@router.get("", response_model=list[ShareResponse])
def list_shares(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return SharingService.list_shares(db, skip, limit)


@router.get("/token/{token}", response_model=ShareResponse)
def get_share_by_token(token: str, db: Session = Depends(get_db)):
    share = SharingService.get_share_response_by_token(db, token)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    return share


@router.post("/{share_id}/comments", response_model=CommentResponse)
def add_comment(share_id: int, payload: CommentCreate, db: Session = Depends(get_db)):
    if not SharingService.share_exists(db, share_id):
        raise HTTPException(status_code=404, detail="Share not found")
    return SharingService.add_comment(db, share_id, payload.user_id, payload.content)


@router.get("/{share_id}/comments", response_model=list[CommentResponse])
def get_comments(share_id: int, db: Session = Depends(get_db)):
    return SharingService.get_comments(db, share_id)
