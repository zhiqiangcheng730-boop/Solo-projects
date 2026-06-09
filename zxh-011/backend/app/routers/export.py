from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import ExportService

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/plan/{plan_id}/pdf")
def export_plan_pdf(plan_id: int, db: Session = Depends(get_db)):
    svc = ExportService(db)
    buf = svc.export_plan_pdf(plan_id)
    if buf is None:
        return {"error": "not found"}
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=plan-{plan_id}.pdf"},
    )
