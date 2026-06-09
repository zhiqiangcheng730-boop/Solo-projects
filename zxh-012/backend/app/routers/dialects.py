from fastapi import APIRouter, Depends, Query
from ..database import get_db
from ..services.dialect_service import DialectService
from ..schemas.schemas import DialectCreate

router = APIRouter(prefix="/api/dialects", tags=["dialects"])


@router.post("/")
def create_dialect(body: DialectCreate, conn=Depends(get_db)):
    svc = DialectService(conn)
    return svc.create(body.model_dump())


@router.get("/")
def list_dialects(province: str = Query(""), conn=Depends(get_db)):
    svc = DialectService(conn)
    if province:
        return svc.list_by_province(province)
    return svc.list_all()


@router.get("/provinces")
def list_provinces(conn=Depends(get_db)):
    svc = DialectService(conn)
    return svc.get_provinces()
