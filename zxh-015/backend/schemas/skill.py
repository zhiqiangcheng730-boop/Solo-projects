from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_serializer


class SkillCreate(BaseModel):
    type: str
    title: str
    description: str = ""
    category: str
    tags: List[str] = []
    city: str
    lat: float = 0.0
    lon: float = 0.0
    is_urgent: bool = False
    urgent_reason: str = ""
    urgent_deadline: Optional[str] = None


class SkillResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    type: str
    title: str
    description: str
    category: str
    tags: str
    city: str
    lat: float
    lon: float
    is_urgent: bool
    urgent_reason: str
    urgent_deadline: Optional[datetime]
    is_active: bool
    created_at: datetime

    @field_serializer("created_at", "urgent_deadline")
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat() if dt else None


class SkillSearch(BaseModel):
    keyword: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    city: Optional[str] = None
    type: Optional[str] = None
