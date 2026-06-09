from pydantic import BaseModel


class LikeToggle(BaseModel):
    user_id: int
    target_id: int  # item_id or plan_id


class LikeCountOut(BaseModel):
    target_id: int
    count: int
    is_liked: bool
