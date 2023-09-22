from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from domain.game import game_schema, game_crud
from domain.auth import auth_router
from models import Game
from starlette.requests import Request
from domain.user import user_router, user_crud
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/game",
)

@router.get("/list")
async def game_dict(db: Session = Depends(get_db)):
    game_dict = await game_crud.get_game_dict(db)
    return game_dict


@router.get("/{category}")
async def game_detail(category: str, db: Session = Depends(get_db)):
    game = await game_crud.get_game(db, category)
    return game


@router.post("/{category}")
async def game_status_change(category:str, game_score: game_schema.Game_score, request: str = Depends(user_router.is_admin), db: Session = Depends(get_db)):
    if not request['validation']:
        return {
            'validation': False,
            "message": "anauthorized"}
    
    # if not await user_router.is_admin(db, request['is_admin']):
    #     return {
    #         'validation': False,
    #         "message": "anauthorized"}
    
    
    game = await game_crud.get_game(db, category)
    if game.result != None:
        return {'message': "ended game can not edit more"}
    
    await game_crud.change_game(db, game, game_score)
    db.refresh(game)
    return game


@router.post('/start/{category}')
async def game_start(category:str, time:datetime, request: str = Depends(user_router.is_admin), db: Session = Depends(get_db)):
    if not request['validation']:
        return {
            'validation': False,
            "message": "anauthorized"}

    game = await game_crud.get_game(db, category)
    if game == None:
        return {'message': "ended game can not edit more"}
    
    await game_crud.start(db, game, time)
    db.refresh(game)
    return game


def cal_percentage(val1, val2):
    total = val1 + val2
    p1 = (val1 / max(total, 1)) * 100
    p2 = (val2 / max(total, 1)) * 100

    if p1 == p2 == 0:
        return [50, 50]
    
    return [p1, p2]

    
@router.get('/ratio/{category}')
async def winpr_ratio(category:str, db: Session = Depends(get_db)):
    users = await user_crud.get_user_list(db)
    a_cnt, b_cnt = 0, 0
    for user in users:
        if user.games[category] != None:
            if user.games[category]:
                a_cnt += 1
            else:
                b_cnt += 1
    result = {}
    res = cal_percentage(a_cnt, b_cnt)
    result['A'] = res[0]
    result['B'] = res[1]

    return result



# @router.post('/predict')
# async def match_predict(body: game_schema.Body, token: str = Depends(auth_router.oauth2_schema), db: Session = Depends(get_db)): # have to send session data to backend (from front(React)) # request: Request
#     res = auth_router.token_validation(token)
#     if not res.validation:
#         return {
#                 'validation': False, 
#                 'message': 'token error'
#                 }
    
#     user = await user_crud.get_user(db, res.message['email'])
#     user.game[body.category] = body.predict # erase user.session
#     db.add(user)
#     db.commit()

#     return {
#         'validation': True, 
#         'message': 'predict success'
#         }
