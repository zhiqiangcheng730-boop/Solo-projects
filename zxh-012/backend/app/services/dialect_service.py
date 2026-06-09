from __future__ import annotations
from ..models.dialect import Dialect, DialectModel


class DialectService:
    def __init__(self, conn):
        self.conn = conn
        self.model = DialectModel

    def create(self, data: dict) -> dict:
        dialect = Dialect(
            name=data["name"],
            province=data["province"],
            description=data.get("description", ""),
        )
        rid = self.model.create(self.conn, dialect)
        dialect.id = rid
        return {"id": dialect.id, "name": dialect.name, "province": dialect.province,
                "description": dialect.description}

    def list_all(self):
        return self.model.list_all(self.conn)

    def list_by_province(self, province: str):
        return self.model.list_by_province(self.conn, province)

    def get_provinces(self):
        return self.model.get_provinces(self.conn)
