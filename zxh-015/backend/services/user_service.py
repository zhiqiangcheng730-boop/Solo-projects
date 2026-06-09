from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.user import User
from schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def register(db: Session, data: UserCreate) -> User:
        existing = db.query(User).filter(
            (User.email == data.email) | (User.username == data.username)
        ).first()
        if existing:
            raise ValueError("用户名或邮箱已存在")
        user = User(
            username=data.username,
            email=data.email,
            password_hash=pwd_context.hash(data.password),
            city=data.city,
            lat=data.lat,
            lon=data.lon,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("邮箱或密码错误")
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("用户不存在")
        return user

    @staticmethod
    def add_coins(db: Session, user_id: int, amount: int) -> User:
        user = UserService.get_by_id(db, user_id)
        user.time_coins += amount
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def deduct_coins(db: Session, user_id: int, amount: int) -> User:
        user = UserService.get_by_id(db, user_id)
        if user.time_coins < amount:
            raise ValueError("时间币不足")
        user.time_coins -= amount
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_credit_score(db: Session, user_id: int, new_rating: float) -> User:
        user = UserService.get_by_id(db, user_id)
        user.credit_score = round((user.credit_score + new_rating * 20) / 2, 1)
        db.commit()
        db.refresh(user)
        return user
