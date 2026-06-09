from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..base_repository import BaseRepository as _Base


@dataclass
class GameQuestion:
    id: Optional[int] = None
    recording_id: int = 0
    correct_meaning: str = ""
    wrong_options: str = ""
    created_at: Optional[str] = None


class GameModel:
    @staticmethod
    def create(conn, question: GameQuestion) -> int:
        return _Base.execute(conn,
            "INSERT INTO game_questions (recording_id, correct_meaning, wrong_options)"
            " VALUES (?, ?, ?)",
            (question.recording_id, question.correct_meaning, question.wrong_options))

    @staticmethod
    def list_all(conn):
        return _Base.fetch_all(conn,
            """SELECT gq.*, r.dialect_name, r.province, r.preset_text
               FROM game_questions gq
               JOIN recordings r ON gq.recording_id = r.id
               ORDER BY gq.created_at DESC""")

    @staticmethod
    def random_questions(conn, limit: int = 5):
        return _Base.fetch_all(conn,
            """SELECT gq.*, r.dialect_name, r.province, r.preset_text, r.audio_file_path
               FROM game_questions gq
               JOIN recordings r ON gq.recording_id = r.id
               ORDER BY RANDOM() LIMIT ?""", (limit,))

    @staticmethod
    def delete(conn, qid: int):
        _Base.execute(conn, "DELETE FROM game_questions WHERE id=?", (qid,))
