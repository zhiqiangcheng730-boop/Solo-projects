from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from ..database import get_db
from ..services.recording_service import RecordingService

router = APIRouter(prefix="/api/recordings", tags=["recordings"])


@router.post("/")
def create_recording(
    dialect_name: str = Form(...),
    province: str = Form(...),
    city: str = Form(""),
    uploader_location: str = Form(""),
    preset_text: str = Form(...),
    is_preset: bool = Form(False),
    recorded_at: str = Form(None),
    audio: UploadFile = File(...),
    conn=Depends(get_db),
):
    svc = RecordingService(conn)
    data = {
        "dialect_name": dialect_name,
        "province": province,
        "city": city,
        "uploader_location": uploader_location,
        "preset_text": preset_text,
        "is_preset": is_preset,
        "recorded_at": recorded_at,
    }
    audio_bytes = audio.file.read() if audio else None
    return svc.create(data, audio_bytes)


@router.get("/")
def list_recordings(
    dialect: str = Query(""),
    province: str = Query(""),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    conn=Depends(get_db),
):
    svc = RecordingService(conn)
    items, total = svc.list_recordings(dialect, province, page, size)
    return {"items": items, "total": total, "page": page, "size": size}


@router.get("/{recording_id}")
def get_recording(recording_id: int, conn=Depends(get_db)):
    svc = RecordingService(conn)
    rec = svc.get(recording_id)
    if not rec:
        return {"error": "not found"}, 404
    return rec


@router.delete("/{recording_id}")
def delete_recording(recording_id: int, conn=Depends(get_db)):
    svc = RecordingService(conn)
    svc.delete(recording_id)
    return {"ok": True}
