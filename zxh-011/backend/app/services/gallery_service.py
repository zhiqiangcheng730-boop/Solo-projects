from sqlalchemy.orm import Session

from ..models import RenovationPlan, Item


class GalleryService:
    def __init__(self, db: Session):
        self.db = db

    def get_plan_detail(self, plan_id: int) -> dict | None:
        plan = self.db.query(RenovationPlan).filter(RenovationPlan.id == plan_id).first()
        if not plan:
            return None
        item = self.db.query(Item).filter(Item.id == plan.item_id).first()
        return {"plan": plan, "item": item}

    def get_featured(self, page: int = 1, page_size: int = 12) -> tuple[list[dict], int]:
        q = self.db.query(RenovationPlan, Item).join(
            Item, RenovationPlan.item_id == Item.id
        ).filter(RenovationPlan.is_featured == 1)
        total = q.count()
        rows = q.order_by(RenovationPlan.likes_count.desc()) \
            .offset((page - 1) * page_size).limit(page_size).all()
        results = []
        for plan, item in rows:
            d = {
                "id": plan.id,
                "item_id": plan.item_id,
                "title": plan.title,
                "content": plan.content,
                "reference_image_url": plan.reference_image_url,
                "result_image_url": plan.result_image_url,
                "author_id": plan.author_id,
                "likes_count": plan.likes_count,
                "is_featured": plan.is_featured,
                "created_at": plan.created_at,
                "item": {
                    "id": item.id,
                    "title": item.title,
                    "category": item.category.value,
                    "image_url": item.image_url,
                }
            }
            results.append(d)
        return results, total

    def get_hot_plans(self, limit: int = 10) -> list[dict]:
        rows = self.db.query(RenovationPlan, Item).join(
            Item, RenovationPlan.item_id == Item.id
        ).order_by(RenovationPlan.likes_count.desc()).limit(limit).all()
        results = []
        for plan, item in rows:
            results.append({
                "id": plan.id,
                "item_id": plan.item_id,
                "title": plan.title,
                "likes_count": plan.likes_count,
                "item_title": item.title,
                "result_image_url": plan.result_image_url,
            })
        return results
