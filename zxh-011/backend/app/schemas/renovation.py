from pydantic import BaseModel, Field
from datetime import datetime


class RenovationPlanCreate(BaseModel):
    item_id: int
    title: str = Field(..., max_length=200)
    content: str
    reference_image_url: str = ""
    result_image_url: str = ""
    author_id: int = 0


class RenovationPlanOut(BaseModel):
    id: int
    item_id: int
    title: str
    content: str
    reference_image_url: str
    result_image_url: str
    author_id: int
    likes_count: int
    is_featured: int
    created_at: datetime

    model_config = {"from_attributes": True}
