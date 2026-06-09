from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.progress import ProgressStepCreate, ProgressStepOut
from ..services import ProgressService

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.post("", response_model=ProgressStepOut, status_code=201)
def add_step(data: ProgressStepCreate, db: Session = Depends(get_db)):
    svc = ProgressService(db)
    return svc.add_step(data)


@router.get("/item/{item_id}", response_model=list[ProgressStepOut])
def list_steps(item_id: int, db: Session = Depends(get_db)):
    svc = ProgressService(db)
    return svc.list_by_item(item_id)


@router.delete("/{step_id}")
def remove_step(step_id: int, db: Session = Depends(get_db)):
    svc = ProgressService(db)
    ok = svc.remove_step(step_id)
    return {"deleted": ok}
