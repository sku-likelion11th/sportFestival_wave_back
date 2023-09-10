from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.major import major_schema
from models import Major

router = APIRouter(
    prefix="/major",
)


@router.get("/list")
def major_list(db: Session = Depends(get_db), response_model=list[major_schema.Major]):
    _major_list = db.query(Major).order_by(Major.id.desc()).all()
    return _major_list
