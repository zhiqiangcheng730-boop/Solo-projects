from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.transaction import Transaction
from schemas.transaction import TransactionCreate
from services.user_service import UserService


class TransactionService:

    @staticmethod
    def create(db: Session, from_user_id: int, data: TransactionCreate) -> Transaction:
        UserService.deduct_coins(db, from_user_id, data.coins)
        txn = Transaction(
            from_user_id=from_user_id,
            to_user_id=data.to_user_id,
            skill_id=data.skill_id,
            hours=data.hours,
            coins=data.coins,
        )
        db.add(txn)
        db.commit()
        db.refresh(txn)
        return txn

    @staticmethod
    def get_by_id(db: Session, txn_id: int) -> Transaction:
        txn = db.query(Transaction).filter(Transaction.id == txn_id).first()
        if not txn:
            raise ValueError("交易不存在")
        return txn

    @staticmethod
    def get_user_transactions(db: Session, user_id: int) -> List[Transaction]:
        return (
            db.query(Transaction)
            .filter(
                (Transaction.from_user_id == user_id)
                | (Transaction.to_user_id == user_id)
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

    @staticmethod
    def accept(db: Session, txn_id: int, user_id: int) -> Transaction:
        txn = TransactionService.get_by_id(db, txn_id)
        if txn.to_user_id != user_id:
            raise ValueError("无权操作")
        if txn.status != "pending":
            raise ValueError("交易状态不允许接受")
        txn.status = "accepted"
        db.commit()
        db.refresh(txn)
        return txn

    @staticmethod
    def complete(db: Session, txn_id: int, user_id: int) -> Transaction:
        txn = TransactionService.get_by_id(db, txn_id)
        if txn.from_user_id != user_id and txn.to_user_id != user_id:
            raise ValueError("无权操作")
        if txn.status != "accepted":
            raise ValueError("交易状态不允许完成")
        txn.status = "completed"
        UserService.add_coins(db, txn.to_user_id, txn.coins)
        txn.completed_at = func.now()
        db.commit()
        db.refresh(txn)
        return txn

    @staticmethod
    def cancel(db: Session, txn_id: int, user_id: int) -> Transaction:
        txn = TransactionService.get_by_id(db, txn_id)
        if txn.from_user_id != user_id:
            raise ValueError("无权操作")
        if txn.status != "pending":
            raise ValueError("交易状态不允许取消")
        txn.status = "cancelled"
        UserService.add_coins(db, txn.from_user_id, txn.coins)
        db.commit()
        db.refresh(txn)
        return txn
