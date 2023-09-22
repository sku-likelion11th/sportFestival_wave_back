from models import Game
from domain.game import game_schema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


async def get_game_dict(db: Session):
    game_list = db.query(Game)\
        .all()
    game_dict = {game.category:game for game in game_list}
    return game_dict


async def get_game(db: Session, category: str):
    game = db.query(Game).get(category)
    return game


async def change_game(db: Session, game:Game, game_score:game_schema.Game_score):
    game.result = game_score.result
    game.score_A = game_score.score_A
    game.score_B = game_score.score_B
    db.commit()
    return game

async def start(db: Session, game:Game, is_start:bool, time: datetime):
    if is_start:
        game.is_start = True
        game.start_time = time
    else:
        game.is_start = False
    db.commit()
    return game