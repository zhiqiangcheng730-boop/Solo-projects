from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_serializer


class TransactionCreate(BaseModel):
    to_user_id: int
    skill_id: Optional[int] = None
    hours: int
    coins: int


class TransactionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    from_user_id: int
    to_user_id: int
    skill_id: Optional[int]
    hours: int
    coins: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    @field_serializer("created_at", "completed_at")
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat() if dt else None
