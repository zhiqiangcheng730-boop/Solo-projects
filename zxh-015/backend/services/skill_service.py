import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.skill import Skill
from schemas.skill import SkillCreate, SkillSearch


class SkillService:

    @staticmethod
    def create(db: Session, user_id: int, data: SkillCreate) -> Skill:
        skill = Skill(
            user_id=user_id,
            type=data.type,
            title=data.title,
            description=data.description,
            category=data.category,
            tags=json.dumps(data.tags),
            city=data.city,
            lat=data.lat,
            lon=data.lon,
            is_urgent=data.is_urgent,
            urgent_reason=data.urgent_reason,
            urgent_deadline=data.urgent_deadline,
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def get_by_id(db: Session, skill_id: int) -> Skill:
        skill = db.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            raise ValueError("技能不存在")
        return skill

    @staticmethod
    def list_skills(
        db: Session,
        city: Optional[str] = None,
        skill_type: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Skill]:
        q = db.query(Skill).filter(Skill.is_active == True)
        if city:
            q = q.filter(Skill.city == city)
        if skill_type:
            q = q.filter(Skill.type == skill_type)
        if category:
            q = q.filter(Skill.category == category)
        return q.order_by(Skill.is_urgent.desc(), Skill.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def search(db: Session, filters: SkillSearch) -> List[Skill]:
        q = db.query(Skill).filter(Skill.is_active == True)
        if filters.city:
            q = q.filter(Skill.city == filters.city)
        if filters.type:
            q = q.filter(Skill.type == filters.type)
        if filters.category:
            q = q.filter(Skill.category == filters.category)
        if filters.keyword:
            keyword = f"%{filters.keyword}%"
            q = q.filter(
                (Skill.title.ilike(keyword)) | (Skill.description.ilike(keyword))
            )
        skills = q.order_by(Skill.is_urgent.desc(), Skill.created_at.desc()).all()
        if filters.tags:
            skills = [
                s for s in skills
                if any(t in json.loads(s.tags) for t in filters.tags)
            ]
        return skills

    @staticmethod
    def get_user_skills(db: Session, user_id: int) -> List[Skill]:
        return db.query(Skill).filter(Skill.user_id == user_id).order_by(Skill.created_at.desc()).all()

    @staticmethod
    def deactivate(db: Session, skill_id: int, user_id: int) -> Skill:
        skill = SkillService.get_by_id(db, skill_id)
        if skill.user_id != user_id:
            raise ValueError("无权操作")
        skill.is_active = False
        db.commit()
        db.refresh(skill)
        return skill

    @staticmethod
    def set_urgent(db: Session, skill_id: int, user_id: int, reason: str, deadline: Optional[str]) -> Skill:
        skill = SkillService.get_by_id(db, skill_id)
        if skill.user_id != user_id:
            raise ValueError("无权操作")
        skill.is_urgent = True
        skill.urgent_reason = reason
        skill.urgent_deadline = deadline
        db.commit()
        db.refresh(skill)
        return skill
