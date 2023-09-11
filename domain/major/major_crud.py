from models import Major
from sqlalchemy.orm import Session


def get_major_list(db: Session):
    major_list = db.query(Major)\
        .order_by(Major.id.desc())\
        .all()
    return major_list


def get_major(db: Session, major_id: int):
    major = db.query(Major).get(major_id)
    return major
