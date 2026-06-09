import json
from typing import List
from sqlalchemy.orm import Session
from models.skill import Skill
from models.user import User


class MatchingService:

    @staticmethod
    def match_for_skill(db: Session, skill_id: int, limit: int = 10) -> List[Skill]:
        target = db.query(Skill).filter(Skill.id == skill_id).first()
        if not target:
            raise ValueError("技能不存在")
        target_tags = set(json.loads(target.tags))
        opposite_type = "request" if target.type == "offer" else "offer"
        candidates = (
            db.query(Skill)
            .filter(
                Skill.is_active == True,
                Skill.type == opposite_type,
                Skill.city == target.city,
                Skill.user_id != target.user_id,
            )
            .all()
        )

        def score(s: Skill) -> float:
            s_tags = set(json.loads(s.tags))
            tag_overlap = len(target_tags & s_tags)
            category_bonus = 3.0 if s.category == target.category else 0.0
            urgent_bonus = 2.0 if s.is_urgent else 0.0
            provider = db.query(User).filter(User.id == s.user_id).first()
            credit_bonus = (provider.credit_score / 100.0) * 2.0 if provider else 0.0
            return tag_overlap + category_bonus + urgent_bonus + credit_bonus

        scored = [(s, score(s)) for s in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:limit]]

    @staticmethod
    def get_recommendations(db: Session, user_id: int, limit: int = 10) -> List[Skill]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("用户不存在")
        user_offer_tags = set()
        for s in db.query(Skill).filter(
            Skill.user_id == user_id, Skill.type == "offer", Skill.is_active == True
        ).all():
            user_offer_tags.update(json.loads(s.tags))

        candidates = (
            db.query(Skill)
            .filter(
                Skill.is_active == True,
                Skill.type == "request",
                Skill.city == user.city,
                Skill.user_id != user_id,
            )
            .all()
        )

        def score(s: Skill) -> float:
            s_tags = set(json.loads(s.tags))
            tag_overlap = len(user_offer_tags & s_tags)
            urgent_bonus = 3.0 if s.is_urgent else 0.0
            requester = db.query(User).filter(User.id == s.user_id).first()
            credit_bonus = (requester.credit_score / 100.0) * 1.5 if requester else 0.0
            return tag_overlap + urgent_bonus + credit_bonus

        scored = [(s, score(s)) for s in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:limit]]
