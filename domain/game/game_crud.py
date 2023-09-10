from models import Game
from sqlalchemy.orm import Session


def get_game_list(db: Session):
    game_list = db.query(Game)\
        .order_by(Game.id.desc())\
        .all()
    return game_list
