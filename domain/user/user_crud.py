from models import User
from sqlalchemy.orm import Session


def get_user_list(db: Session):
    user_list = db.query(User)\
        .order_by(User.id.desc())\
        .all()
    return user_list
