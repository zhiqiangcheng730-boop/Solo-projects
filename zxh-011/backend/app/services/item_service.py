from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models import Item, ItemCategory, Difficulty
from ..schemas.item import ItemCreate, ItemUpdate, ItemFilter


class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get(self, item_id: int) -> Item | None:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def list_filtered(self, filters: ItemFilter) -> tuple[list[Item], int]:
        q = self.db.query(Item)
        if filters.category:
            q = q.filter(Item.category == filters.category)
        if filters.difficulty:
            q = q.filter(Item.difficulty == filters.difficulty)
        if filters.material:
            q = q.filter(Item.material.ilike(f"%{filters.material}%"))
        if filters.keyword:
            kw = f"%{filters.keyword}%"
            q = q.filter(or_(Item.title.ilike(kw), Item.description.ilike(kw)))
        if filters.status:
            q = q.filter(Item.status == filters.status)
        total = q.count()
        items = q.order_by(Item.created_at.desc()) \
            .offset((filters.page - 1) * filters.page_size) \
            .limit(filters.page_size).all()
        return items, total

    def update(self, item_id: int, data: ItemUpdate) -> Item | None:
        item = self.get(item_id)
        if not item:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(item, k, v)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get(item_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
