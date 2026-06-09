from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.item import ItemCreate, ItemUpdate, ItemOut, ItemFilter
from ..schemas.progress import ProgressStepOut
from ..services import ItemService, ProgressService, TagService
from ..models import ItemCategory, Difficulty

router = APIRouter(prefix="/api/items", tags=["items"])


@router.post("", response_model=ItemOut, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    svc = ItemService(db)
    return svc.create(data)


@router.get("", response_model=dict)
def list_items(
    category: ItemCategory | None = Query(None),
    difficulty: Difficulty | None = Query(None),
    material: str | None = Query(None),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filters = ItemFilter(
        category=category, difficulty=difficulty, material=material,
        keyword=keyword, status=status, page=page, page_size=page_size,
    )
    svc = ItemService(db)
    items, total = svc.list_filtered(filters)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/{item_id}", response_model=dict)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item_svc = ItemService(db)
    item = item_svc.get(item_id)
    if not item:
        return {"error": "not found"}
    progress_svc = ProgressService(db)
    tag_svc = TagService(db)
    return {
        "item": item,
        "progress": progress_svc.list_by_item(item_id),
        "tags": tag_svc.get_item_tags(item_id),
    }


@router.put("/{item_id}", response_model=ItemOut)
def update_item(item_id: int, data: ItemUpdate, db: Session = Depends(get_db)):
    svc = ItemService(db)
    return svc.update(item_id, data)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    svc = ItemService(db)
    ok = svc.delete(item_id)
    return {"deleted": ok}
