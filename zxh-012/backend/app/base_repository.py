from __future__ import annotations


class BaseRepository:
    """Thin SQL helpers shared by model classes. Not a framework — just reduces boilerplate."""

    @staticmethod
    def fetch_all(conn, sql: str, params: tuple = ()) -> list[dict]:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

    @staticmethod
    def fetch_one(conn, sql: str, params: tuple = ()) -> dict | None:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    @staticmethod
    def fetch_scalar(conn, sql: str, params: tuple = ()):
        row = conn.execute(sql, params).fetchone()
        return row[0] if row else None

    @staticmethod
    def execute(conn, sql: str, params: tuple = ()) -> int:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid

    @staticmethod
    def paginate(conn, table: str, where_clause: str, params: tuple,
                 page: int, size: int, order_by: str = "created_at DESC"):
        offset = (page - 1) * size
        clause = f" WHERE {where_clause}" if where_clause else ""
        rows = conn.execute(
            f"SELECT * FROM {table}{clause} ORDER BY {order_by} LIMIT ? OFFSET ?",
            (*params, size, offset),
        ).fetchall()
        total = conn.execute(
            f"SELECT COUNT(*) FROM {table}{clause}", params
        ).fetchone()[0]
        return [dict(r) for r in rows], total
