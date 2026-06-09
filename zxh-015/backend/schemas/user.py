from datetime import datetime
from pydantic import BaseModel, field_serializer


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    city: str
    lat: float = 0.0
    lon: float = 0.0


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    username: str
    email: str
    city: str
    lat: float
    lon: float
    time_coins: int
    credit_score: float
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime, _info):
        return dt.isoformat()
