from fastapi import APIRouter, Depends
from ..database import get_db
from ..services.statistics_service import StatisticsService

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("/dashboard")
def dashboard(conn=Depends(get_db)):
    svc = StatisticsService(conn)
    return svc.dashboard()


@router.get("/heatmap")
def heatmap(conn=Depends(get_db)):
    svc = StatisticsService(conn)
    return svc.heatmap_all()
