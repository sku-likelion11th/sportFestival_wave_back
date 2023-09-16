from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.game import game_schema, game_crud
from models import Game

router = APIRouter(
    prefix="/game",
)

major = {
    "컴공" : "컴공image_url"
}


@router.get("/list")
async def game_dict(db: Session = Depends(get_db)):
    _game_list = game_crud.get_game_dict(db)
    return _game_list


@router.get("/{category}")
async def game_detail(category: str, db: Session = Depends(get_db)):
    game = game_crud.get_game(db, category)
    return game

@router.post("/{category}")
async def game_status_change(category:str, game_score: game_schema.Game_score, db: Session = Depends(get_db)):
    game = await game_crud.get_game(db, category)
    await game_crud.change_game(db, game, game_score)
    db.refresh(game)
    return game
