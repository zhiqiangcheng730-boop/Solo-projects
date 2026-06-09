from fastapi import APIRouter, Depends
from ..database import get_db
from ..services.vocabulary_service import VocabularyService
from ..schemas.schemas import VocabularyCreate

router = APIRouter(prefix="/api/vocabulary", tags=["vocabulary"])


@router.post("/")
def create_annotation(body: VocabularyCreate, conn=Depends(get_db)):
    svc = VocabularyService(conn)
    return svc.create(body.model_dump())


@router.get("/{recording_id}")
def list_annotations(recording_id: int, conn=Depends(get_db)):
    svc = VocabularyService(conn)
    return svc.list_by_recording(recording_id)


@router.delete("/{annotation_id}")
def delete_annotation(annotation_id: int, conn=Depends(get_db)):
    svc = VocabularyService(conn)
    svc.delete(annotation_id)
    return {"ok": True}
