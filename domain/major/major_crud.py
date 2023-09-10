from models import Major
from sqlalchemy.orm import Session


def get_mahjor_list(db: Session):
    major_list = db.query(Major)\
        .order_by(Major.id.desc())\
        .all()
    return major_list
