from pydantic import BaseModel
from datetime import datetime


class ProgressStepCreate(BaseModel):
    item_id: int
    step_order: int
    description: str = ""
    image_url: str


class ProgressStepOut(BaseModel):
    id: int
    item_id: int
    step_order: int
    description: str
    image_url: str
    created_at: datetime

    model_config = {"from_attributes": True}
