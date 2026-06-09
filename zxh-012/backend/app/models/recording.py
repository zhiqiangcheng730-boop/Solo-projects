from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from ..base_repository import BaseRepository as _Base


@dataclass
class Recording:
    id: Optional[int] = None
    dialect_name: str = ""
    province: str = ""
    city: str = ""
    uploader_location: str = ""
    audio_file_path: str = ""
    preset_text: str = ""
    is_preset: bool = False
    recorded_at: Optional[str] = None
    created_at: Optional[str] = None


class RecordingModel:
    @staticmethod
    def create(conn, recording: Recording) -> int:
        return _Base.execute(conn,
            "INSERT INTO recordings (dialect_name, province, city, uploader_location,"
            " audio_file_path, preset_text, is_preset, recorded_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (recording.dialect_name, recording.province, recording.city,
             recording.uploader_location, recording.audio_file_path,
             recording.preset_text, int(recording.is_preset),
             recording.recorded_at or datetime.now().isoformat()))

    @staticmethod
    def list_all(conn, dialect: str = "", province: str = "", page: int = 1, size: int = 20):
        conditions = []
        params = []
        if dialect:
            conditions.append("dialect_name = ?")
            params.append(dialect)
        if province:
            conditions.append("province = ?")
            params.append(province)
        where = " AND ".join(conditions) if conditions else ""
        return _Base.paginate(conn, "recordings", where, tuple(params), page, size)

    @staticmethod
    def get_by_id(conn, rid: int):
        return _Base.fetch_one(conn, "SELECT * FROM recordings WHERE id=?", (rid,))

    @staticmethod
    def delete(conn, rid: int):
        _Base.execute(conn, "DELETE FROM recordings WHERE id=?", (rid,))
