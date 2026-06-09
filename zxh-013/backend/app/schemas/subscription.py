from pydantic import BaseModel, Field
from datetime import datetime


class SubscriptionCreate(BaseModel):
    name: str = Field(default="", max_length=64)
    center_lat: float = Field(ge=-90, le=90)
    center_lng: float = Field(ge=-180, le=180)
    radius_km: float = Field(gt=0, le=100)


class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    name: str
    center_lat: float
    center_lng: float
    radius_km: float
    created_at: datetime

    model_config = {"from_attributes": True}
