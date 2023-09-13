from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.game import game_schema, game_crud
from models import Game

router = APIRouter(
    prefix="/game",
)


# @router.get("/list")
# def game_list(db: Session = Depends(get_db), response_model=list[game_schema.Game]):
#     _game_list = game_crud.get_game_list(db)
#     return _game_list


# @router.get("/detail/{game_id}", response_model=game_schema.Game)
# def game_detail(game_id: int, db: Session = Depends(get_db)):
#     game = game_crud.get_game(db, game_id=game_id)
#     return game