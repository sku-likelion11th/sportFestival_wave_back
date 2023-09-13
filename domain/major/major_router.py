from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.major import major_schema, major_crud
from models import Major

router = APIRouter(
    prefix="/major",
)


# @router.get("/list")
# def major_list(db: Session = Depends(get_db), response_model=list[major_schema.Major]):
#     _major_list = major_crud.get_major_list(db)
#     return _major_list


# @router.get("/detail/{major_id}", response_model=major_schema.Major)
# def major_detail(major_id: int, db: Session = Depends(get_db)):
#     major = major_crud.get_major(db, major_id=major_id)
#     return major