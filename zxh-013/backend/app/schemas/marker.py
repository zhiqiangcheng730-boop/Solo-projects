from pydantic import BaseModel, Field
from datetime import datetime


class MarkerCreate(BaseModel):
    category: str = Field(min_length=1, max_length=32)
    title: str = Field(min_length=1, max_length=128)
    description: str = Field(default="", max_length=512)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class MarkerOut(BaseModel):
    id: int
    user_id: int
    category: str
    title: str
    description: str
    latitude: float
    longitude: float
    vote_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
