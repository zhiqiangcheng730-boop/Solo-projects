from typing import List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.transaction import Transaction
from models.user import User


class RankingService:

    @staticmethod
    def get_top_helpers(db: Session, limit: int = 20) -> List[Dict]:
        rows = (
            db.query(
                Transaction.to_user_id,
                func.sum(Transaction.hours).label("total_hours"),
                func.count(Transaction.id).label("total_txns"),
            )
            .filter(Transaction.status == "completed")
            .group_by(Transaction.to_user_id)
            .order_by(func.sum(Transaction.hours).desc())
            .limit(limit)
            .all()
        )
        result = []
        for rank, row in enumerate(rows, 1):
            user = db.query(User).filter(User.id == row.to_user_id).first()
            if user:
                result.append({
                    "rank": rank,
                    "user_id": user.id,
                    "username": user.username,
                    "city": user.city,
                    "total_hours": int(row.total_hours),
                    "total_txns": int(row.total_txns),
                    "credit_score": user.credit_score,
                })
        return result

    @staticmethod
    def get_highest_credit(db: Session, limit: int = 20) -> List[Dict]:
        users = db.query(User).order_by(User.credit_score.desc()).limit(limit).all()
        return [
            {
                "rank": i + 1,
                "user_id": u.id,
                "username": u.username,
                "city": u.city,
                "credit_score": u.credit_score,
                "time_coins": u.time_coins,
            }
            for i, u in enumerate(users)
        ]
