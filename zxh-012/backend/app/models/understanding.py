from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..base_repository import BaseRepository as _Base


@dataclass
class UnderstandingMark:
    id: Optional[int] = None
    recording_id: int = 0
    province: str = ""
    understood: bool = False
    created_at: Optional[str] = None


class UnderstandingModel:
    @staticmethod
    def create(conn, mark: UnderstandingMark) -> int:
        return _Base.execute(conn,
            "INSERT INTO understanding_marks (recording_id, province, understood) VALUES (?, ?, ?)",
            (mark.recording_id, mark.province, int(mark.understood)))

    @staticmethod
    def count_by_recording(conn, recording_id: int):
        total = _Base.fetch_scalar(conn,
            "SELECT COUNT(*) FROM understanding_marks WHERE recording_id=?", (recording_id,))
        understood = _Base.fetch_scalar(conn,
            "SELECT COUNT(*) FROM understanding_marks WHERE recording_id=? AND understood=1", (recording_id,))
        return {"total": total or 0, "understood": understood or 0}

    @staticmethod
    def heatmap_data(conn, recording_id: int = 0):
        if recording_id:
            rows = conn.execute(
                """SELECT province, COUNT(*) as total,
                   SUM(CASE WHEN understood=1 THEN 1 ELSE 0 END) as understood_count
                   FROM understanding_marks WHERE recording_id=?
                   GROUP BY province""", (recording_id,)).fetchall()
        else:
            rows = conn.execute(
                """SELECT province, COUNT(*) as total,
                   SUM(CASE WHEN understood=1 THEN 1 ELSE 0 END) as understood_count
                   FROM understanding_marks GROUP BY province""").fetchall()
        return [{"province": r["province"], "total": r["total"],
                 "understood": r["understood_count"],
                 "ratio": round(r["understood_count"] / r["total"], 2) if r["total"] > 0 else 0}
                for r in rows]
