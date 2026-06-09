from typing import List
from sqlalchemy.orm import Session
from models.skill import Skill


class UrgentService:

    @staticmethod
    def get_urgent_needs(db: Session, city: str = None) -> List[Skill]:
        q = db.query(Skill).filter(
            Skill.is_active == True,
            Skill.is_urgent == True,
        )
        if city:
            q = q.filter(Skill.city == city)
        return q.order_by(Skill.created_at.desc()).all()

    @staticmethod
    def mark_urgent(db: Session, skill_id: int, user_id: int, reason: str) -> Skill:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            raise ValueError("技能不存在")
        if skill.user_id != user_id:
            raise ValueError("无权操作")
        skill.is_urgent = True
        skill.urgent_reason = reason
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def unmark_urgent(db: Session, skill_id: int, user_id: int) -> Skill:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            raise ValueError("技能不存在")
        if skill.user_id != user_id:
            raise ValueError("无权操作")
        skill.is_urgent = False
        db.commit()
        db.refresh(skill)
        return skill
