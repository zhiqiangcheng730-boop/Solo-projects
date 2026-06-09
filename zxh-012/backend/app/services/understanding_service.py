from __future__ import annotations
from ..models.understanding import UnderstandingMark, UnderstandingModel


class UnderstandingService:
    def __init__(self, conn):
        self.conn = conn
        self.model = UnderstandingModel

    def mark(self, data: dict) -> dict:
        mark = UnderstandingMark(
            recording_id=data["recording_id"],
            province=data["province"],
            understood=data.get("understood", False),
        )
        mid = self.model.create(self.conn, mark)
        mark.id = mid
        return {"id": mark.id, "recording_id": mark.recording_id,
                "province": mark.province, "understood": mark.understood}

    def get_stats(self, recording_id: int):
        return self.model.count_by_recording(self.conn, recording_id)

    def heatmap(self, recording_id: int = 0):
        return self.model.heatmap_data(self.conn, recording_id)
