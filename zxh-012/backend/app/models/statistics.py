from __future__ import annotations
from ..base_repository import BaseRepository as _Base


class StatisticsModel:
    @staticmethod
    def dashboard(conn):
        total_recordings = _Base.fetch_scalar(conn, "SELECT COUNT(*) FROM recordings") or 0
        total_dialects = _Base.fetch_scalar(conn,
            "SELECT COUNT(DISTINCT dialect_name) FROM recordings") or 0
        total_marks = _Base.fetch_scalar(conn,
            "SELECT COUNT(*) FROM understanding_marks") or 0
        total_questions = _Base.fetch_scalar(conn,
            "SELECT COUNT(*) FROM game_questions") or 0
        provinces = _Base.fetch_all(conn,
            "SELECT DISTINCT province FROM recordings ORDER BY province")

        province_stats = []
        for p in provinces:
            prov = p["province"]
            count = _Base.fetch_scalar(conn,
                "SELECT COUNT(*) FROM recordings WHERE province=?", (prov,)) or 0
            mark_count = _Base.fetch_scalar(conn,
                """SELECT COUNT(*) FROM understanding_marks um
                   JOIN recordings r ON um.recording_id = r.id
                   WHERE r.province=?""", (prov,)) or 0
            province_stats.append({
                "province": prov, "recording_count": count, "mark_count": mark_count})

        return {
            "total_recordings": total_recordings,
            "total_dialects": total_dialects,
            "total_marks": total_marks,
            "total_questions": total_questions,
            "province_stats": province_stats,
        }

    @staticmethod
    def heatmap_all(conn):
        rows = conn.execute(
            """SELECT province, COUNT(*) as total,
               SUM(CASE WHEN understood=1 THEN 1 ELSE 0 END) as understood_count
               FROM understanding_marks GROUP BY province""").fetchall()
        return [{"province": r["province"], "total": r["total"],
                 "understood": r["understood_count"],
                 "ratio": round(r["understood_count"] / r["total"], 2) if r["total"] > 0 else 0}
                for r in rows]
