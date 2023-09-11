from models import User
from sqlalchemy.orm import Session


def get_user_list(db: Session):
    user_list = db.query(User)\
        .order_by(User.id.desc())\
        .all()
    return user_list


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user