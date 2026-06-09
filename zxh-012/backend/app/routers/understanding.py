from fastapi import APIRouter, Depends, Query
from ..database import get_db
from ..services.understanding_service import UnderstandingService
from ..schemas.schemas import UnderstandingMarkCreate

router = APIRouter(prefix="/api/understanding", tags=["understanding"])


@router.post("/")
def mark_understanding(body: UnderstandingMarkCreate, conn=Depends(get_db)):
    svc = UnderstandingService(conn)
    return svc.mark(body.model_dump())


@router.get("/stats/{recording_id}")
def get_stats(recording_id: int, conn=Depends(get_db)):
    svc = UnderstandingService(conn)
    return svc.get_stats(recording_id)


@router.get("/heatmap")
def heatmap(recording_id: int = Query(0), conn=Depends(get_db)):
    svc = UnderstandingService(conn)
    return svc.heatmap(recording_id)
