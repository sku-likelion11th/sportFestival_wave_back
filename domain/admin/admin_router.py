from database import get_db
from domain.game import game_schema, game_crud
from domain.user import user_router, user_crud
from domain.major import major_router, major_crud
from domain.admin import admin_schema
from domain.auth import auth_router
from models import User, Game, Major
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
import json

router = APIRouter(
    prefix="/admin",
)

@router.post('/modify') # admin page score modify function
async def admin_modify(body: admin_schema.Body, token: str = Depends(auth_router.oauth2_schema), db: Session = Depends(get_db)):
    res = user_router.is_admin(token)
    if not res['is_admin']:
        return {
                'validation': False, 
                'message': 'no admin'
                }

    game = await game_crud.get_game(db, body.category)
    if body.result == "done":
        game.result = True
        return {
            'validation': True, 
            'message': 'end game'}

    if body.team == 'A': # team_A
        game.score_A = body.score
    else:
        game.score_B = body.score
    
    db.add(game)
    db.commit()

    return {
        'validation': True, 
        'message': 'modified'}