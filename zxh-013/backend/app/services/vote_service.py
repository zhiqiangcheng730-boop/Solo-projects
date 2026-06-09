from sqlalchemy.orm import Session
from ..models.vote import Vote
from ..models.marker import Marker
from ..models.user import User


def cast_vote(db: Session, user_id: int, marker_id: int) -> bool:
    existing = db.query(Vote).filter(Vote.user_id == user_id, Vote.marker_id == marker_id).first()
    if existing:
        return False
    vote = Vote(user_id=user_id, marker_id=marker_id)
    db.add(vote)
    db.query(Marker).filter(Marker.id == marker_id).update(
        {"vote_count": Marker.vote_count + 1}
    )
    marker = db.query(Marker).filter(Marker.id == marker_id).first()
    if marker:
        db.query(User).filter(User.id == marker.user_id).update(
            {"score": User.score + 1}
        )
    db.commit()
    return True


def remove_vote(db: Session, user_id: int, marker_id: int) -> bool:
    vote = db.query(Vote).filter(Vote.user_id == user_id, Vote.marker_id == marker_id).first()
    if not vote:
        return False
    db.delete(vote)
    db.query(Marker).filter(Marker.id == marker_id).update(
        {"vote_count": Marker.vote_count - 1}
    )
    marker = db.query(Marker).filter(Marker.id == marker_id).first()
    if marker and marker.user_id:
        db.query(User).filter(User.id == marker.user_id).update(
            {"score": User.score - 1}
        )
    db.commit()
    return True


def has_voted(db: Session, user_id: int, marker_id: int) -> bool:
    return db.query(Vote).filter(Vote.user_id == user_id, Vote.marker_id == marker_id).first() is not None
