from models import User
from sqlalchemy.orm import Session


async def get_user_list(db: Session):
    user_list = db.query(User)\
        .all()
    return user_list


async def get_user(db: Session, email: str):
    user = db.query(User).get(email)
    return user