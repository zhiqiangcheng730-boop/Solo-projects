from __future__ import annotations
from ..models.game import GameQuestion, GameModel


class GameService:
    def __init__(self, conn):
        self.conn = conn
        self.model = GameModel

    def create(self, data: dict) -> dict:
        question = GameQuestion(
            recording_id=data["recording_id"],
            correct_meaning=data["correct_meaning"],
            wrong_options=data["wrong_options"],
        )
        qid = self.model.create(self.conn, question)
        question.id = qid
        return {"id": question.id, "recording_id": question.recording_id,
                "correct_meaning": question.correct_meaning,
                "wrong_options": question.wrong_options}

    def list_all(self):
        return self.model.list_all(self.conn)

    def random_questions(self, limit: int = 5):
        return self.model.random_questions(self.conn, limit)

    def delete(self, qid: int):
        self.model.delete(self.conn, qid)
