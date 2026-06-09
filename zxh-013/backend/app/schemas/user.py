from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    nickname: str = Field(default="", max_length=64)


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}
