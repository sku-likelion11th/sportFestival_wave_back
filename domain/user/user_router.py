from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema
from models import User

router = APIRouter(
    prefix="/user",
)


@router.get("/list")
def user_list(db: Session = Depends(get_db), response_model=list[user_schema.User]):
    _user_list = db.query(User).order_by(User.id.desc()).all()
    return _user_list
