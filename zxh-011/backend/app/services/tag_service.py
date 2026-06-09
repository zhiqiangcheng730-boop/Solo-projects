from sqlalchemy.orm import Session

from ..models import Tag, ItemTag


class TagService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, name: str) -> Tag:
        tag = self.db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def list_all(self) -> list[Tag]:
        return self.db.query(Tag).all()

    def tag_item(self, item_id: int, tag_ids: list[int]):
        for tag_id in tag_ids:
            exists = self.db.query(ItemTag).filter(
                ItemTag.item_id == item_id, ItemTag.tag_id == tag_id
            ).first()
            if not exists:
                self.db.add(ItemTag(item_id=item_id, tag_id=tag_id))
        self.db.commit()

    def get_item_tags(self, item_id: int) -> list[Tag]:
        return self.db.query(Tag).join(ItemTag).filter(ItemTag.item_id == item_id).all()

    def get_items_by_tag(self, tag_id: int) -> list[int]:
        rows = self.db.query(ItemTag.item_id).filter(ItemTag.tag_id == tag_id).all()
        return [r[0] for r in rows]
