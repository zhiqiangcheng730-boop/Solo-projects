from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.transaction import TransactionCreate, TransactionResponse
from services.transaction_service import TransactionService

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.post("/", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, from_user_id: int = Query(...), db: Session = Depends(get_db)):
    return TransactionService.create(db, from_user_id, data)


@router.get("/", response_model=List[TransactionResponse])
def list_transactions(user_id: int = Query(...), db: Session = Depends(get_db)):
    return TransactionService.get_user_transactions(db, user_id)


@router.get("/{txn_id}", response_model=TransactionResponse)
def get_transaction(txn_id: int, db: Session = Depends(get_db)):
    return TransactionService.get_by_id(db, txn_id)


@router.put("/{txn_id}/accept", response_model=TransactionResponse)
def accept_transaction(txn_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return TransactionService.accept(db, txn_id, user_id)


@router.put("/{txn_id}/complete", response_model=TransactionResponse)
def complete_transaction(txn_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return TransactionService.complete(db, txn_id, user_id)


@router.put("/{txn_id}/cancel", response_model=TransactionResponse)
def cancel_transaction(txn_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return TransactionService.cancel(db, txn_id, user_id)
