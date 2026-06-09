from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import SymbolResponse, ExplanationCreate, ExplanationResponse, VoteRequest
from app.services.symbol_service import SymbolService

router = APIRouter(prefix="/api/symbols", tags=["symbols"])


@router.get("", response_model=list[SymbolResponse])
def list_symbols(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return SymbolService.list_symbols(db, skip, limit)


@router.get("/{keyword}", response_model=SymbolResponse)
def get_symbol(keyword: str, db: Session = Depends(get_db)):
    symbol = SymbolService.get_symbol_by_keyword(db, keyword)
    if not symbol:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol


@router.get("/{symbol_id}/explanations")
def get_explanations(symbol_id: int, db: Session = Depends(get_db)):
    return SymbolService.get_explanations(db, symbol_id)


@router.post("/explanations", response_model=ExplanationResponse)
def add_explanation(payload: ExplanationCreate, db: Session = Depends(get_db)):
    if not SymbolService.symbol_exists(db, payload.symbol_id):
        raise HTTPException(status_code=404, detail="Symbol not found")
    return SymbolService.add_explanation(db, payload.symbol_id, payload.user_id, payload.explanation, payload.source)


@router.post("/explanations/vote")
def vote_explanation(payload: VoteRequest, db: Session = Depends(get_db)):
    voted = SymbolService.vote_explanation(db, payload.explanation_id, payload.user_id)
    return {"voted": voted}


@router.get("/{symbol_id}/explanations/top")
def get_top_explanations(symbol_id: int, db: Session = Depends(get_db), limit: int = 5):
    return SymbolService.get_top_explanations(db, symbol_id, limit)
