from fastapi import APIRouter, Depends, Query
from ..database import get_db
from ..services.game_service import GameService
from ..schemas.schemas import GameQuestionCreate

router = APIRouter(prefix="/api/game", tags=["game"])


@router.post("/questions")
def create_question(body: GameQuestionCreate, conn=Depends(get_db)):
    svc = GameService(conn)
    return svc.create(body.model_dump())


@router.get("/questions")
def list_questions(conn=Depends(get_db)):
    svc = GameService(conn)
    return svc.list_all()


@router.get("/challenge")
def random_challenge(limit: int = Query(5, ge=1, le=20), conn=Depends(get_db)):
    svc = GameService(conn)
    return svc.random_questions(limit)


@router.delete("/questions/{question_id}")
def delete_question(question_id: int, conn=Depends(get_db)):
    svc = GameService(conn)
    svc.delete(question_id)
    return {"ok": True}
