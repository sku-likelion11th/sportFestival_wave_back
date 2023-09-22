from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from database import get_db
from domain.user import user_schema, user_crud, user_router
from domain.auth import auth_router
from domain.game import game_schema
from models import User
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.requests import Request
from starlette.config import Config
from starlette.responses import HTMLResponse, RedirectResponse
import json

router = APIRouter(
    prefix="/user",
)

# # don't use
# @router.get("/list")
# def user_list(db: Session = Depends(get_db), response_model=list[user_schema.User]):
#     _user_list = user_crud.get_user_list(db)
#     return _user_list

# # don't use
# @router.get("/detail/{user_id}", response_model=user_schema.User)
# def user_detail(user_id: int, db: Session = Depends(get_db)):
#     user = user_crud.get_user_by_id(db, user_id=user_id)
#     if user is None:
#         return HTMLResponse('no_user_detail')#RedirectResponse(url='/')
#     return user

from domain.auth.auth_router import auth_google
from domain.auth import auth_router

@router.post('/info')
async def user_change(user_data: user_schema.User,request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)):
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    user.student_num = user_data.student_num
    user.phone_num = user_data.phone_num

    db.commit()
    return {'validation': True,
            'message': 'success'}
    
    
@router.get('/info') #, response_model=list[user_schema.User]):
async def user_info(request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)) -> user_schema.User:
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    return user.__dict__ # 모든 column 출력

    

# @router.get('/game') # i think user/info url can displace this functions
# async def user_game(request: str = Depends(auth_router.token_validation), db:Session = Depends(get_db)):
#     user = await user_crud.get_user(db, request['message']['email'])
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")
#     else:
#         return user.games
    

@router.post('/game')
async def user_game(body: game_schema.Body, request: str = Depends(auth_router.token_validation), db:Session = Depends(get_db)):
    if not request['validation']:
        return request
    
    user = await user_crud.get_user(db, request['message']['email'])

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    if user:
        if (not user.student_num) or (not user.phone_num):
            return {"message":"edit your info for trying predict"}
        user.games[body.category] = body.predict
        flag_modified(user, "games")
        db.add(user)
        db.commit()
        return user.games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")


def cal_percentage(val1, val2):
    total = val1 + val2
    p1 = (val1 / max(total, 1)) * 100
    p2 = (val2 / max(total, 1)) * 100

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
    if res[0] == res[1] == 0:
        result['A'] = 50
        result['B'] = 50

        return result
    
    result['A'] = res[0]
    result['B'] = res[1]

    return result


async def is_admin(token: str = Depends(auth_router.oauth2_schema), db: Session = Depends(get_db)):
    res = auth_router.token_validation(token)
    if not res.validation:
        return {
                'validation': False, 
                'message': 'token error'
                }
    
    user = await user_crud.get_user(db, res.message['email'])

    if user.is_admin:
        return {'is_admin': True}
    else:
        return {'is_admin': False}


@router.post('/valid')
async def number_valid(request: str = Depends(auth_router.token_validation), db: Session = Depends(get_db)):
    user = await user_crud.get_user(db, request['message']['email'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not logged in")

    if (not user.student_num) or (not user.phone_num):
        return {'validation': False,
                'message': 'invalid'}
    
    return {'validation': True,
            'message': 'valid'}
