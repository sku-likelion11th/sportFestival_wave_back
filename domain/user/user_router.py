from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.user import user_schema, user_crud
from models import User

router = APIRouter(
    prefix="/user",
)


@router.get("/list")
def user_list(db: Session = Depends(get_db), response_model=list[user_schema.User]):
    _user_list = user_crud.get_user_list(db)
    return _user_list


@router.get("/detail/{user_id}", response_model=user_schema.User)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id=user_id)
    return user