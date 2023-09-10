from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.game import game_schema
from models import Game

router = APIRouter(
    prefix="/game",
)


@router.get("/list")
def game_list(db: Session = Depends(get_db), response_model=list[game_schema.Game]):
    _game_list = db.query(Game).order_by(Game.id.desc()).all()
    return _game_list
