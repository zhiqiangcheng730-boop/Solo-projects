from __future__ import annotations
from ..models.vocabulary import VocabularyAnnotation, VocabularyModel


class VocabularyService:
    def __init__(self, conn):
        self.conn = conn
        self.model = VocabularyModel

    def create(self, data: dict) -> dict:
        vocab = VocabularyAnnotation(
            recording_id=data["recording_id"],
            dialect_word=data["dialect_word"],
            standard_word=data["standard_word"],
        )
        vid = self.model.create(self.conn, vocab)
        vocab.id = vid
        return {"id": vocab.id, "recording_id": vocab.recording_id,
                "dialect_word": vocab.dialect_word, "standard_word": vocab.standard_word}

    def list_by_recording(self, recording_id: int):
        return self.model.list_by_recording(self.conn, recording_id)

    def delete(self, vid: int):
        self.model.delete(self.conn, vid)
