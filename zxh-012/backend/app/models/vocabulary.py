from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from ..base_repository import BaseRepository as _Base


@dataclass
class VocabularyAnnotation:
    id: Optional[int] = None
    recording_id: int = 0
    dialect_word: str = ""
    standard_word: str = ""
    created_at: Optional[str] = None


class VocabularyModel:
    @staticmethod
    def create(conn, vocab: VocabularyAnnotation) -> int:
        return _Base.execute(conn,
            "INSERT INTO vocabulary_annotations (recording_id, dialect_word, standard_word)"
            " VALUES (?, ?, ?)",
            (vocab.recording_id, vocab.dialect_word, vocab.standard_word))

    @staticmethod
    def list_by_recording(conn, recording_id: int):
        return _Base.fetch_all(conn,
            "SELECT * FROM vocabulary_annotations WHERE recording_id=? ORDER BY created_at",
            (recording_id,))

    @staticmethod
    def delete(conn, vid: int):
        _Base.execute(conn, "DELETE FROM vocabulary_annotations WHERE id=?", (vid,))
