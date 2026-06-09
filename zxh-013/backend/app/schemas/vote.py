from pydantic import BaseModel
from datetime import datetime


class VoteCreate(BaseModel):
    marker_id: int


class VoteOut(BaseModel):
    id: int
    user_id: int
    marker_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
