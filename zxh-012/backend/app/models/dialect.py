from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..base_repository import BaseRepository as _Base


@dataclass
class Dialect:
    id: Optional[int] = None
    name: str = ""
    province: str = ""
    description: str = ""


class DialectModel:
    @staticmethod
    def create(conn, dialect: Dialect) -> int:
        return _Base.execute(conn,
            "INSERT INTO dialects (name, province, description) VALUES (?, ?, ?)",
            (dialect.name, dialect.province, dialect.description))

    @staticmethod
    def list_all(conn):
        return _Base.fetch_all(conn, "SELECT * FROM dialects ORDER BY province, name")

    @staticmethod
    def list_by_province(conn, province: str):
        return _Base.fetch_all(conn,
            "SELECT * FROM dialects WHERE province=? ORDER BY name", (province,))

    @staticmethod
    def get_provinces(conn):
        rows = conn.execute(
            "SELECT DISTINCT province FROM dialects ORDER BY province").fetchall()
        return [r["province"] for r in rows]
