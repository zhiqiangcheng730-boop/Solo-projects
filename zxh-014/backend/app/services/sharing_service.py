from sqlalchemy.orm import Session, joinedload
from app.models.sharing import AnonymousShare, ShareComment
from app.models.dream import DreamRecord


class SharingService:
    """Manage anonymous dream sharing and community comments."""

    @staticmethod
    def share_exists(db: Session, share_id: int) -> bool:
        return db.query(AnonymousShare).filter(AnonymousShare.id == share_id).first() is not None

    @staticmethod
    def _format_share(share: AnonymousShare) -> dict:
        return {
            "id": share.id,
            "share_token": share.share_token,
            "dream_content": share.dream.content if share.dream else "",
            "dream_emotion": share.dream.emotion if share.dream else "",
            "comment_count": len(share.comments) if share.comments else 0,
            "created_at": share.created_at,
        }

    @staticmethod
    def create_share_response(db: Session, dream_id: int) -> dict:
        share = AnonymousShare(dream_id=dream_id)
        db.add(share)
        db.commit()
        db.refresh(share)
        return {
            "id": share.id,
            "share_token": share.share_token,
            "dream_content": share.dream.content,
            "dream_emotion": share.dream.emotion,
            "comment_count": 0,
            "created_at": share.created_at,
        }

    @staticmethod
    def get_share_by_token(db: Session, token: str) -> AnonymousShare | None:
        return db.query(AnonymousShare).filter(AnonymousShare.share_token == token).first()

    @staticmethod
    def get_share_response_by_token(db: Session, token: str) -> dict | None:
        share = SharingService.get_share_by_token(db, token)
        if not share:
            return None
        return SharingService._format_share(share)

    @staticmethod
    def list_shares(db: Session, skip: int = 0, limit: int = 20) -> list[dict]:
        shares = (
            db.query(AnonymousShare)
            .options(joinedload(AnonymousShare.dream), joinedload(AnonymousShare.comments))
            .order_by(AnonymousShare.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [SharingService._format_share(s) for s in shares]

    @staticmethod
    def add_comment(db: Session, share_id: int, user_id: str, content: str) -> ShareComment:
        comment = ShareComment(share_id=share_id, user_id=user_id, content=content)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def get_comments(db: Session, share_id: int) -> list[ShareComment]:
        return (
            db.query(ShareComment)
            .filter(ShareComment.share_id == share_id)
            .order_by(ShareComment.created_at.asc())
            .all()
        )
