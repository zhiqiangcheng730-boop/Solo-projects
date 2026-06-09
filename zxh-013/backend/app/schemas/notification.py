from pydantic import BaseModel
from datetime import datetime


class NotificationOut(BaseModel):
    id: int
    marker_id: int
    marker_title: str
    marker_category: str
    latitude: float
    longitude: float
    created_at: datetime
