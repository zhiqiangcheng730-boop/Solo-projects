from __future__ import annotations
import uuid
from pathlib import Path
from ..config import UPLOAD_DIR
from ..models.recording import Recording, RecordingModel


class RecordingService:
    def __init__(self, conn):
        self.conn = conn
        self.model = RecordingModel

    def create(self, data: dict, audio_data: bytes = None) -> dict:
        filename = f"{uuid.uuid4().hex}.webm"
        filepath = UPLOAD_DIR / filename
        if audio_data:
            filepath.write_bytes(audio_data)
        recording = Recording(
            dialect_name=data["dialect_name"],
            province=data["province"],
            city=data.get("city", ""),
            uploader_location=data.get("uploader_location", ""),
            audio_file_path=f"/uploads/{filename}",
            preset_text=data["preset_text"],
            is_preset=data.get("is_preset", False),
            recorded_at=data.get("recorded_at"),
        )
        rid = self.model.create(self.conn, recording)
        recording.id = rid
        return self._to_dict(recording)

    def list_recordings(self, dialect: str = "", province: str = "", page: int = 1, size: int = 20):
        return self.model.list_all(self.conn, dialect, province, page, size)

    def get(self, rid: int):
        return self.model.get_by_id(self.conn, rid)

    def delete(self, rid: int):
        rec = self.model.get_by_id(self.conn, rid)
        if rec and rec.get("audio_file_path"):
            fp = UPLOAD_DIR.parent / rec["audio_file_path"].lstrip("/")
            if fp.exists():
                fp.unlink()
        self.model.delete(self.conn, rid)

    def _to_dict(self, recording: Recording) -> dict:
        return {
            "id": recording.id,
            "dialect_name": recording.dialect_name,
            "province": recording.province,
            "city": recording.city,
            "uploader_location": recording.uploader_location,
            "audio_file_path": recording.audio_file_path,
            "preset_text": recording.preset_text,
            "is_preset": recording.is_preset,
            "recorded_at": recording.recorded_at,
            "created_at": recording.created_at,
        }
