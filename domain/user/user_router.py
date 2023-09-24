from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from database import get_db
from domain.user import user_schema, user_crud, user_router
from domain.auth import auth_router
from domain.game import game_schema, game_crud
from models import User
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
import json
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/user",
)


from domain.auth.auth_router import auth_google
from domain.auth import auth_router

@router.post('/info')
async def user_change(user_data: user_schema.User, request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    user.student_num = user_data.student_num
    user.phone_num = user_data.phone_num

    db.commit()
    return {'validation': True,
            'message': 'success'}
    
    
@router.get('/info') #, response_model=list[user_schema.User]):
async def user_info(request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    return user.__dict__

    

@router.get('/game') # i think user/info url can displace this functions
async def user_game(request: str = Depends(auth_router.token_validation), db:Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")
    else:
        return user.games
    

@router.post('/game')
async def user_game_change(body: game_schema.Body, request: str = Depends(auth_router.token_validation), db:Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    game = await game_crud.get_game(db, body.category)
    if game.start_time - timedelta(minutes=10) <= datetime.now():
        return {
            "validation": False,
            "message":"predict impossible. time over"}

    user = await user_crud.get_user(db, request['message']['email'])

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    if user:
        if (not user.student_num) or (not user.phone_num):
            return {
                "validation": False,
                "message":"edit your info for trying predict"}
        user.games[body.category] = body.predict
        flag_modified(user, "games")
        db.add(user)
        db.commit()
        return user.games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


async def is_admin(db: Session = Depends(get_db), res: dict = Depends(auth_router.token_validation)):
    if not res['validation']:
        return {
                'validation': False, 
                'message': 'token error'
                }
    
    user = await user_crud.get_user(db, res['message']['email'])
    if user.is_admin:
        return {
            'validation': True, 
            'is_admin': True}
    else:
        return {
            'validation': False, 
            'is_admin': False}


@router.get('/valid')
async def number_valid(request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    if (not user.student_num) or (not user.phone_num):
        return {'validation': False,
                'message': 'invalid'}
    
    return {'validation': True,
            'message': 'valid'}
