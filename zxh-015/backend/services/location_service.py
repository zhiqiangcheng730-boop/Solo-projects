import json
from typing import List, Dict
from sqlalchemy.orm import Session
from models.skill import Skill
from models.user import User
from utils import haversine_distance


class LocationService:

    @staticmethod
    def get_nearby_providers(
        db: Session,
        lat: float,
        lon: float,
        radius_km: float = 10.0,
        limit: int = 20,
    ) -> List[Dict]:
        skills = db.query(Skill).filter(
            Skill.is_active == True,
            Skill.type == "offer",
        ).all()
        results = []
        for s in skills:
            if s.lat and s.lon:
                dist = haversine_distance(lat, lon, s.lat, s.lon)
                if dist <= radius_km:
                    provider = db.query(User).filter(User.id == s.user_id).first()
                    results.append({
                        "skill_id": s.id,
                        "title": s.title,
                        "category": s.category,
                        "tags": json.loads(s.tags),
                        "city": s.city,
                        "lat": round(s.lat, 3),
                        "lon": round(s.lon, 3),
                        "distance_km": round(dist, 1),
                        "provider_credit": provider.credit_score if provider else 100.0,
                    })
        results.sort(key=lambda x: x["distance_km"])
        return results[:limit]

    @staticmethod
    def get_city_skills(db: Session, city: str) -> List[Dict]:
        skills = (
            db.query(Skill)
            .filter(
                Skill.is_active == True,
                Skill.city == city,
            )
            .all()
        )
        return [
            {
                "skill_id": s.id,
                "title": s.title,
                "type": s.type,
                "category": s.category,
                "tags": json.loads(s.tags),
                "city": s.city,
                "lat": round(s.lat, 3) if s.lat else 0,
                "lon": round(s.lon, 3) if s.lon else 0,
                "is_urgent": s.is_urgent,
            }
            for s in skills
        ]
