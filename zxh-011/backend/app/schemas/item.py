from pydantic import BaseModel, Field
from datetime import datetime
from ..models.item import ItemCategory, Difficulty


class ItemCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str = ""
    category: ItemCategory
    difficulty: Difficulty = Difficulty.EASY
    material: str = ""
    size_desc: str = ""
    image_url: str
    creator_id: int = 0


class ItemUpdate(BaseModel):
    title: str | None = Field(None, max_length=200)
    description: str | None = None
    difficulty: Difficulty | None = None
    material: str | None = None
    size_desc: str | None = None
    status: str | None = None


class ItemOut(BaseModel):
    id: int
    title: str
    description: str
    category: ItemCategory
    difficulty: Difficulty
    material: str
    size_desc: str
    image_url: str
    status: str
    creator_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ItemFilter(BaseModel):
    category: ItemCategory | None = None
    difficulty: Difficulty | None = None
    material: str | None = None
    keyword: str | None = None
    status: str | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=12, ge=1, le=100)
