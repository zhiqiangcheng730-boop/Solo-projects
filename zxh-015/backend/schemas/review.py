from datetime import datetime
from pydantic import BaseModel, field_serializer


class ReviewCreate(BaseModel):
    transaction_id: int
    rating: int
    comment: str = ""


class ReviewResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    transaction_id: int
    reviewer_id: int
    reviewee_id: int
    rating: int
    comment: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime, _info):
        return dt.isoformat()
