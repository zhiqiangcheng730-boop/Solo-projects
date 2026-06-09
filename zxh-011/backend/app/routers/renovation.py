from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.renovation import RenovationPlanCreate, RenovationPlanOut
from ..services import RenovationService

router = APIRouter(prefix="/api/renovations", tags=["renovations"])


@router.post("", response_model=RenovationPlanOut, status_code=201)
def create_plan(data: RenovationPlanCreate, db: Session = Depends(get_db)):
    svc = RenovationService(db)
    return svc.create(data)


@router.get("/item/{item_id}", response_model=list[RenovationPlanOut])
def list_plans(item_id: int, db: Session = Depends(get_db)):
    svc = RenovationService(db)
    return svc.list_by_item(item_id)


@router.get("/{plan_id}", response_model=RenovationPlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    svc = RenovationService(db)
    return svc.get(plan_id)
