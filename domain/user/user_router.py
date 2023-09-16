from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from database import get_db
from domain.user import user_schema, user_crud
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

@router.post('/info')
async def user_change(request: Request, user_data: user_schema.User, db: Session = Depends(get_db)):
    user = await auth_google(request.session.get('user'))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = user_crud.get_user(db,user['email'])
    userdb.student_num = user_data.student_num
    userdb.phone_num = user_data.phone_num

    db.commit()
    return userdb
    
    
@router.get('/info')
async def user_info(request: Request, db: Session = Depends(get_db)):#, response_model=list[user_schema.User]):
    user = await auth_google(request.session.get('user'))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = await user_crud.get_user(db,user['email'])

    if userdb:
        return userdb.__dict__ # 모든 column 출력
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")
    

@router.get('/game')
async def user_game(request: Request, db:Session = Depends(get_db)):
    user = await auth_google(request.session.get('user'))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = await user_crud.get_user(db,user['email'])
    if userdb:
        return userdb.games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")
    

@router.post('/game')
async def user_game(request: Request, category: str, select: str, db:Session = Depends(get_db)):
    user = await auth_google(request.session.get('user'))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인안함")
    userdb = await user_crud.get_user(db,user['email'])
    if userdb:
        userdb.games[category] = select
        flag_modified(userdb, "games")
        db.add(userdb)
        db.commit()
        return userdb.games
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없음")
    
    
@router.get('/ratio/{category}')
async def winpr_ratio(category:str, db: Session = Depends(get_db)):
    users = await user_crud.get_user_list(db)
    result = {}
    for user in users:
        if user.games[category]:
            try:
                result[user.games[category]]+=1
            except:
                result[user.games[category]]=1
    return result



